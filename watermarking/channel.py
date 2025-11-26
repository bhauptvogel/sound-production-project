# watermarking/channel.py

from dataclasses import dataclass
from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F

from .stft_utils import STFTConfig, stft, istft


@dataclass
class ChannelConfig:
    stft_cfg: STFTConfig = STFTConfig()
    
    # Channel mode: "none" (identity), "noise_only", or "full" (all attacks)
    mode: str = "full"

    # Additive noise
    enable_noise: bool = True
    noise_std_min: float = 0.0
    noise_std_max: float = 0.02  # tune later

    # Random EQ (multi-band gain in frequency domain)
    enable_eq: bool = True
    eq_num_bands: int = 6
    eq_gain_db_min: float = -6.0
    eq_gain_db_max: float = 6.0

    # Resampling / speed perturbation (waveform-domain)
    enable_resample: bool = True
    resample_min_rate: float = 0.9   # e.g. 0.9x
    resample_max_rate: float = 1.1   # e.g. 1.1x

    # Bit-depth quantization (straight-through estimator)
    enable_quantize: bool = True
    quant_bits_min: int = 12
    quant_bits_max: int = 16

    # Probabilities to skip some attacks in each forward
    p_noise: float = 0.8
    p_eq: float = 0.7
    p_resample: float = 0.5
    p_quant: float = 0.7


def _ensure_batch(waveform: torch.Tensor) -> Tuple[torch.Tensor, bool]:
    """
    Accepts (T,), (1,T), or (B,T). Returns (B,T) and flag indicating whether
    original had batch dim.
    """
    if waveform.ndim == 1:
        return waveform.unsqueeze(0), False
    elif waveform.ndim == 2:
        return waveform, True
    elif waveform.ndim == 3 and waveform.shape[1] == 1:
        # (B,1,T) -> (B,T)
        return waveform[:, 0, :], True
    else:
        raise ValueError(f"Unexpected waveform shape: {waveform.shape}")


# ---------- Individual attacks ----------

def additive_noise(
    x: torch.Tensor,
    std_min: float,
    std_max: float,
) -> torch.Tensor:
    """
    x: (B, T)
    std is sampled per-batch-element from [std_min, std_max].
    """
    if std_max <= 0:
        return x

    B, T = x.shape
    device = x.device

    std = torch.empty(B, 1, device=device).uniform_(std_min, std_max)
    noise = torch.randn_like(x) * std
    return x + noise


def random_eq_stft(
    x: torch.Tensor,
    cfg: ChannelConfig,
) -> torch.Tensor:
    """
    Simple multi-band EQ in STFT domain.

    x: (B, T)
    returns: (B, T)
    """
    stft_cfg = cfg.stft_cfg
    X = stft(x, stft_cfg)        # (B, F, T_frames), complex
    B, F, T_frames = X.shape
    device = X.device

    num_bands = cfg.eq_num_bands
    if num_bands <= 1:
        return x

    # Assign each frequency bin to a band index [0, num_bands-1]
    freqs = torch.arange(F, device=device)  # (F,)
    band_edges = torch.linspace(0, F, steps=num_bands + 1, device=device)
    band_idxs = torch.bucketize(freqs, band_edges[1:-1])  # (F,), values in [0, num_bands-1]

    # Sample a gain (in dB) per band and per batch
    gains_db = torch.empty(B, num_bands, device=device).uniform_(
        cfg.eq_gain_db_min, cfg.eq_gain_db_max
    )  # (B, num_bands)

    gains_lin = 10.0 ** (gains_db / 20.0)  # (B, num_bands)
    gains_lin = gains_lin[:, :, None]      # (B, num_bands, 1)

    # Map band gains to per-frequency gains: (B, F, 1)
    band_idxs_expanded = band_idxs[None, :, None].expand(B, -1, 1)  # (B, F, 1)
    gains_per_bin = torch.gather(gains_lin, 1, band_idxs_expanded)  # (B, F, 1)

    # Apply EQ in frequency domain
    X_eq = X * gains_per_bin  # broadcast over time frames

    # Back to time domain
    y = istft(X_eq, stft_cfg, length=x.shape[-1])  # (B, T)
    return y


def random_resample(
    x: torch.Tensor,
    rate_min: float,
    rate_max: float,
) -> torch.Tensor:
    """
    Simple waveform-domain speed perturbation via linear interpolation.

    x: (B, T)
    returns: (B, T) with content slightly stretched/compressed.
    """
    if rate_min <= 0 or rate_max <= 0:
        return x

    B, T = x.shape
    device = x.device

    rates = torch.empty(B, device=device).uniform_(rate_min, rate_max)  # (B,)

    y_out = []
    for b in range(B):
        r = rates[b]
        # Choose new length (speed up -> shorter, slow down -> longer)
        T_new = int(T / r)
        if T_new < 2:
            y_out.append(x[b : b + 1, :])
            continue

        xb = x[b : b + 1, :].unsqueeze(1)  # (1,1,T)

        # Resample to T_new via linear interpolation
        yb = F.interpolate(
            xb,
            size=T_new,
            mode="linear",
            align_corners=False,
        )  # (1,1,T_new)

        # Now center-crop or pad back to original length T
        if T_new > T:
            start = (T_new - T) // 2
            yb = yb[..., start : start + T]  # (1,1,T)
        elif T_new < T:
            pad_left = (T - T_new) // 2
            pad_right = T - T_new - pad_left
            yb = F.pad(yb, (pad_left, pad_right))  # (1,1,T)

        y_out.append(yb[:, 0, :])  # (1,T)

    y = torch.cat(y_out, dim=0)  # (B,T)
    return y


def quantize_ste(
    x: torch.Tensor,
    bits_min: int,
    bits_max: int,
) -> torch.Tensor:
    """
    Straight-through estimator (STE) bit-depth quantization.

    x: (B, T) assumed in [-1, 1]
    """
    B, T = x.shape
    device = x.device

    bits = torch.randint(bits_min, bits_max + 1, (B,), device=device)  # inclusive
    y = x.clone()

    for b in range(B):
        n_bits = int(bits[b].item())
        max_int = 2 ** (n_bits - 1) - 1
        scale = float(max_int)

        xb = x[b]
        yb = torch.round(xb * scale) / scale

        # STE: forward uses yb, backward uses gradient of identity
        y[b] = xb + (yb - xb).detach()

    return y


class DifferentiableChannel(nn.Module):
    """
    Composes several differentiable-ish attacks:

      - optional additive noise
      - optional random EQ (frequency-domain gain)
      - optional resampling / time-stretch-like perturbation
      - optional quantization via STE

    All ops are defined so that gradients can still flow back to the encoder.
    """

    def __init__(self, cfg: ChannelConfig):
        super().__init__()
        self.cfg = cfg

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        """
        waveform: (T,), (1,T), (B,T), or (B,1,T)
        returns: (B,T) or (1,T) depending on input
        """
        x, had_batch = _ensure_batch(waveform)   # (B,T)

        B, T = x.shape
        device = x.device

        # Mode "none": identity (no attacks)
        if self.cfg.mode == "none":
            x = x.clamp(-1.2, 1.2)
            return x[0] if not had_batch else x

        # Additive noise (applies in "noise_only" and "full" modes)
        if self.cfg.mode in ("noise_only", "full") and self.cfg.enable_noise:
            mask = (torch.rand(B, device=device) < self.cfg.p_noise).float().view(B, 1)
            if mask.any():
                x_noisy = additive_noise(x, self.cfg.noise_std_min, self.cfg.noise_std_max)
                x = mask * x_noisy + (1.0 - mask) * x

        # Other attacks only in "full" mode
        if self.cfg.mode == "full":
            # Random EQ
            if self.cfg.enable_eq:
                mask = (torch.rand(B, device=device) < self.cfg.p_eq).float().view(B, 1)
                if mask.any():
                    x_eq = random_eq_stft(x, self.cfg)
                    x = mask * x_eq + (1.0 - mask) * x

            # Resample / time-stretch
            if self.cfg.enable_resample:
                mask = (torch.rand(B, device=device) < self.cfg.p_resample).float().view(B, 1)
                if mask.any():
                    x_res = random_resample(x, self.cfg.resample_min_rate, self.cfg.resample_max_rate)
                    x = mask * x_res + (1.0 - mask) * x

            # Quantization via STE
            if self.cfg.enable_quantize:
                mask = (torch.rand(B, device=device) < self.cfg.p_quant).float().view(B, 1)
                if mask.any():
                    x_q = quantize_ste(x, self.cfg.quant_bits_min, self.cfg.quant_bits_max)
                    x = mask * x_q + (1.0 - mask) * x

        # Clamp to a reasonable range
        x = x.clamp(-1.2, 1.2)

        if not had_batch:
            return x[0]
        return x


def mp3_roundtrip(
    waveform: torch.Tensor,
    sr: int,
    bitrate_kbps: int = 128,
) -> torch.Tensor:
    """
    waveform: (T,), (1,T), or (B,T) in [-1,1]
    Non-differentiable: detach before calling if used during training.
    """
    import tempfile
    import soundfile as sf
    import subprocess
    import os

    batched, had_batch = _ensure_batch(waveform)
    device = batched.device
    dtype = batched.dtype
    B, T = batched.shape
    waveform_np = batched.detach().cpu().numpy()

    outs = []

    for b in range(B):
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_path = os.path.join(tmpdir, "in.wav")
            mp3_path = os.path.join(tmpdir, "out.mp3")
            wav2_path = os.path.join(tmpdir, "out.wav")

            sf.write(wav_path, waveform_np[b], sr)

            # encode
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", wav_path,
                 "-b:a", f"{bitrate_kbps}k", mp3_path],
                check=True,
            )
            # decode
            subprocess.run(
                ["ffmpeg", "-y", "-loglevel", "error", "-i", mp3_path, wav2_path],
                check=True,
            )

            y, sr2 = sf.read(wav2_path)
            if y.ndim > 1:
                y = y.mean(axis=1)
            y_t = torch.from_numpy(y).float()

            # Crop/pad per item back to original length T
            if y_t.shape[0] < T:
                y_t = F.pad(y_t, (0, T - y_t.shape[0]))
            elif y_t.shape[0] > T:
                y_t = y_t[:T]

            outs.append(y_t)

    y_out = torch.stack(outs, dim=0).to(device=device, dtype=dtype)  # (B, T)
    if not had_batch:
        return y_out[0]
    return y_out
