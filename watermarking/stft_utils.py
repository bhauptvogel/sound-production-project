from dataclasses import dataclass
from typing import Tuple

import torch
import torchaudio


@dataclass
class STFTConfig:
    n_fft: int = 1024
    hop_length: int = 256
    win_length: int = 1024
    center: bool = True
    window_fn: str = "hann"  # later you can generalize


def _get_window(cfg: STFTConfig, device: torch.device) -> torch.Tensor:
    if cfg.window_fn == "hann":
        win = torch.hann_window(cfg.win_length, periodic=True, device=device)
    else:
        raise ValueError(f"Unsupported window: {cfg.window_fn}")
    return win


def stft(
    waveform: torch.Tensor,
    cfg: STFTConfig,
) -> torch.Tensor:
    """
    waveform: (B, T) or (1, T) or (T,)
    returns: complex STFT of shape (B, F, T_frames)
    """
    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)

    B, T = waveform.shape
    device = waveform.device

    window = _get_window(cfg, device=device)

    X = torch.stft(
        input=waveform,
        n_fft=cfg.n_fft,
        hop_length=cfg.hop_length,
        win_length=cfg.win_length,
        window=window,
        center=cfg.center,
        return_complex=True,
    )  # (B, F, T_frames)

    return X


def istft(
    spec: torch.Tensor,
    cfg: STFTConfig,
    length: int | None = None,
) -> torch.Tensor:
    """
    spec: (B, F, T_frames), complex
    returns: waveform (B, T)
    """
    device = spec.device
    window = _get_window(cfg, device=device)

    x = torch.istft(
        input=spec,
        n_fft=cfg.n_fft,
        hop_length=cfg.hop_length,
        win_length=cfg.win_length,
        window=window,
        center=cfg.center,
        length=length,
    )  # (B, T)

    return x

def stft_logmag(
    waveform: torch.Tensor,
    cfg: STFTConfig,
) -> torch.Tensor:
    """
    waveform: (B, T) or (T,)
    returns: log-magnitude STFT, shape (B, F, T_frames)
    """
    X = stft(waveform, cfg)          # complex (B, F, T_frames)
    mag = X.abs()
    logmag = torch.log(mag + 1e-7)
    return logmag


# ---------- Log-mel features (for analysis / neural net input) ----------

@dataclass
class MelConfig:
    sample_rate: int = 44_100
    n_fft: int = 1024
    hop_length: int = 256
    win_length: int = 1024
    n_mels: int = 64
    f_min: float = 20.0
    f_max: float = 20_000.0
    center: bool = True


class LogMelSpec(torch.nn.Module):
    """
    Non-invertible analysis feature. Use this for encoder/decoder inputs.
    Do NOT rely on this to reconstruct the waveform.
    """

    def __init__(self, cfg: MelConfig):
        super().__init__()
        self.cfg = cfg
        self.register_buffer(
            "window",
            torch.hann_window(cfg.win_length, periodic=True),
            persistent=False,
        )
        self.mel_scale = torchaudio.transforms.MelScale(
            n_mels=cfg.n_mels,
            sample_rate=cfg.sample_rate,
            f_min=cfg.f_min,
            f_max=cfg.f_max,
            n_stft=cfg.n_fft // 2 + 1,
        )

    def forward(self, waveform: torch.Tensor) -> torch.Tensor:
        """
        waveform: (B, T) or (T,)
        returns: log-mel spectrogram (B, n_mels, T_frames)
        """
        if waveform.ndim == 1:
            waveform = waveform.unsqueeze(0)

        B, T = waveform.shape
        device = waveform.device

        window = self.window.to(device)
        mel_scale = self.mel_scale.to(device)

        spec = torch.stft(
            input=waveform,
            n_fft=self.cfg.n_fft,
            hop_length=self.cfg.hop_length,
            win_length=self.cfg.win_length,
            window=window,
            center=self.cfg.center,
            return_complex=True,
        )  # (B, F, T_frames)

        mag = spec.abs()  # (B, F, T_frames)
        mel = mel_scale(mag)  # (B, n_mels, T_frames)
        log_mel = torch.log(mel + 1e-7)
        return log_mel
