# watermarking/models.py

from dataclasses import dataclass, field
from typing import Tuple

import torch
import torch.nn as nn

from .stft_utils import STFTConfig, stft, istft, stft_logmag


# ---------- Configs ----------

@dataclass
class EncoderConfig:
    n_bits: int
    bit_emb_dim: int = 32
    base_channels: int = 64
    stft_cfg: STFTConfig = field(default_factory=STFTConfig)


@dataclass
class DecoderConfig:
    n_bits: int
    base_channels: int = 64
    stft_cfg: STFTConfig = field(default_factory=STFTConfig)


def _bit_bin_pairs(cfg: EncoderConfig | DecoderConfig) -> Tuple[torch.Tensor, torch.Tensor]:
    freq_bins = cfg.stft_cfg.n_fft // 2 + 1
    guard = 8
    usable_start = guard
    usable_end = freq_bins - guard
    required_bins = cfg.n_bits * 2

    if usable_end - usable_start < required_bins:
        raise ValueError(
            "Not enough frequency bins for the requested number of bits. "
            f"Available={usable_end - usable_start}, required={required_bins}. "
            "Increase n_fft or reduce n_bits."
        )

    available_bins = usable_end - usable_start
    linspace_idx = torch.linspace(
        0, available_bins - 1, steps=required_bins, dtype=torch.float32
    )
    discrete_idx = torch.round(linspace_idx).to(torch.long)

    # Ensure strictly increasing indices to avoid degenerate pairs
    for i in range(1, discrete_idx.numel()):
        if discrete_idx[i] <= discrete_idx[i - 1]:
            discrete_idx[i] = discrete_idx[i - 1] + 1

    if discrete_idx[-1] >= available_bins:
        raise ValueError(
            "Failed to assign unique frequency bins for all bits. "
            "Try increasing n_fft or reducing n_bits."
        )

    indices = discrete_idx + usable_start
    pos_bins = indices[0::2]
    neg_bins = indices[1::2]

    if torch.any(pos_bins == neg_bins):
        raise RuntimeError("Bit bin pairing produced identical bin indices.")

    return pos_bins, neg_bins


# ---------- Encoder: bits + log|X| -> mask M ----------

class WatermarkEncoder(nn.Module):
    """
    Encoder CNN that takes:
      - log-magnitude STFT (B, 1, F, T)
      - bits (B, n_bits) in {0,1}
    and outputs:
      - mask M (B, 1, F, T)

    M is unconstrained; we apply tanh(M) * eps later.
    """

    def __init__(self, cfg: EncoderConfig):
        super().__init__()
        self.cfg = cfg

        # Stronger bit conditioning: map bits to a larger embedding space
        self.bit_mlp = nn.Sequential(
            nn.Linear(cfg.n_bits, cfg.bit_emb_dim * 2),
            nn.ReLU(),
            nn.Linear(cfg.bit_emb_dim * 2, cfg.bit_emb_dim * 2),
            nn.ReLU(),
            nn.Linear(cfg.bit_emb_dim * 2, cfg.bit_emb_dim),
        )

        in_channels = 1 + cfg.bit_emb_dim  # log|X| channel + broadcasted bit embedding

        # Process audio features
        self.audio_conv = nn.Sequential(
            nn.Conv2d(1, cfg.base_channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(cfg.base_channels, cfg.base_channels, kernel_size=3, padding=1),
            nn.ReLU(),
        )
        
        # Process bit conditioning separately, then combine
        self.bit_conv = nn.Sequential(
            nn.Conv2d(cfg.bit_emb_dim, cfg.base_channels, kernel_size=1),
            nn.ReLU(),
        )
        
        # Combine audio and bit features
        self.combine_conv = nn.Sequential(
            nn.Conv2d(cfg.base_channels * 2, cfg.base_channels, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(cfg.base_channels, cfg.base_channels // 2, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(cfg.base_channels // 2, 1, kernel_size=3, padding=1),
            # no activation here; we will tanh() outside
        )
        
        freq_bins = cfg.stft_cfg.n_fft // 2 + 1
        pos_bins, neg_bins = _bit_bin_pairs(cfg)
        bit_matrix = torch.zeros(cfg.n_bits, freq_bins)
        for i in range(cfg.n_bits):
            bit_matrix[i, pos_bins[i]] = 1.0
            bit_matrix[i, neg_bins[i]] = -1.0
        self.register_buffer("bit_index_matrix", bit_matrix)
        self.bit_strength = nn.Parameter(torch.ones(cfg.n_bits) * 0.1)
        
        nn.init.xavier_uniform_(self.combine_conv[-1].weight, gain=1.0)
        if self.combine_conv[-1].bias is not None:
            nn.init.zeros_(self.combine_conv[-1].bias)
        
        self.mask_scale = nn.Parameter(torch.ones(1))

    def forward(self, logmag: torch.Tensor, bits: torch.Tensor) -> torch.Tensor:
        """
        logmag: (B, 1, F, T)
        bits: (B, n_bits) in {0,1}
        returns:
            M: (B, 1, F, T)
        """
        if logmag.ndim != 4:
            raise ValueError(f"logmag must be (B,1,F,T), got {logmag.shape}")
        if bits.ndim != 2:
            raise ValueError(f"bits must be (B,n_bits), got {bits.shape}")
        if bits.shape[1] != self.cfg.n_bits:
            raise ValueError(f"bits second dim ({bits.shape[1]}) != cfg.n_bits ({self.cfg.n_bits})")

        B, _, F, T = logmag.shape
        expected_F = self.cfg.stft_cfg.n_fft // 2 + 1
        if F != expected_F:
            raise ValueError(
                f"logmag frequency dimension ({F}) does not match encoder STFT config ({expected_F})."
            )

        # Process audio features
        audio_feat = self.audio_conv(logmag)  # (B, base_channels, F, T)

        # Process bit conditioning - make it spatial
        bits = bits.float()
        bit_emb = self.bit_mlp(bits)          # (B, bit_emb_dim)
        # Broadcast to spatial dimensions
        bit_map = bit_emb[:, :, None, None]   # (B, bit_emb_dim, 1, 1)
        bit_map = bit_map.expand(-1, -1, F, T)  # (B, bit_emb_dim, F, T)
        bit_feat = self.bit_conv(bit_map)     # (B, base_channels, F, T)

        # Combine audio and bit features
        combined = torch.cat([audio_feat, bit_feat], dim=1)  # (B, 2*base_channels, F, T)
        
        # Generate mask
        residual = self.combine_conv(combined)  # (B, 1, F, T)
        
        bits_centered = bits * 2 - 1  # (B,n_bits) in {-1,1}
        strength = torch.sigmoid(self.bit_strength)  # (n_bits,)
        weighted_bits = bits_centered * strength  # (B,n_bits)
        template = torch.matmul(weighted_bits, self.bit_index_matrix)  # (B,F)
        template = template.unsqueeze(1).unsqueeze(-1)  # (B,1,F,1)
        template = template.expand(-1, 1, residual.shape[2], residual.shape[3])
        
        M = (template + residual) * self.mask_scale  # Apply learnable scale
        return M


# ---------- Decoder: log|Y_attacked| -> bits logits ----------

class WatermarkDecoder(nn.Module):
    """
    Decoder CNN that takes:
      - log-magnitude STFT of (possibly attacked) audio: (B, 1, F, T)
    and outputs:
      - logits: (B, n_bits)
    """

    def __init__(self, cfg: DecoderConfig):
        super().__init__()
        self.cfg = cfg

        C = cfg.base_channels

        self.features = nn.Sequential(
            nn.Conv2d(1, C, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(C, C, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),  # (F/2, T/2)

            nn.Conv2d(C, 2 * C, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.Conv2d(2 * C, 2 * C, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),  # (F/4, T/4)

            nn.Conv2d(2 * C, 2 * C, kernel_size=3, padding=1),
            nn.ReLU(),
        )

        # Global average over F,T → (B, 2C)
        self.head = nn.Linear(2 * C, cfg.n_bits)
        nn.init.zeros_(self.head.bias)

        pos_bins, neg_bins = _bit_bin_pairs(cfg)
        self.register_buffer("pos_bins", pos_bins)
        self.register_buffer("neg_bins", neg_bins)
        self.diff_linear = nn.Linear(cfg.n_bits, cfg.n_bits)
        nn.init.eye_(self.diff_linear.weight)
        nn.init.zeros_(self.diff_linear.bias)

    def forward(self, logmag: torch.Tensor) -> torch.Tensor:
        """
        logmag: (B, 1, F, T)
        returns:
            logits: (B, n_bits)
        """
        if logmag.ndim != 4:
            raise ValueError(f"logmag must be (B,1,F,T), got {logmag.shape}")

        x = self.features(logmag)          # (B, 2C, F', T')
        x = x.mean(dim=(-2, -1))          # global average pooling over F,T -> (B, 2C)
        cnn_logits = self.head(x)

        B, _, F, T = logmag.shape
        expected_F = self.cfg.stft_cfg.n_fft // 2 + 1
        if F != expected_F:
            raise ValueError(
                f"logmag frequency dimension ({F}) does not match decoder STFT config ({expected_F})."
            )

        logmag_sq = logmag.squeeze(1)  # (B,F,T)
        pos_energy = logmag_sq[:, self.pos_bins, :].mean(dim=-1)
        neg_energy = logmag_sq[:, self.neg_bins, :].mean(dim=-1)
        diff = pos_energy - neg_energy  # (B,n_bits)
        diff_logits = self.diff_linear(diff)

        return cnn_logits + diff_logits


# ---------- Mask application: log|Y| = log|X| + eps * tanh(M) ----------

def apply_watermark_mask(
    X_complex: torch.Tensor,
    M: torch.Tensor,
    eps: float,
) -> torch.Tensor:
    """
    Apply log-magnitude mask to complex STFT.

    X_complex: (B, F, T) complex STFT
    M: (B, 1, F, T) mask from encoder
    eps: scalar controlling watermark strength

    returns:
        Y_complex: (B, F, T) complex STFT of watermarked signal
    """
    if X_complex.ndim != 3:
        raise ValueError(f"X_complex must be (B,F,T), got {X_complex.shape}")
    if not torch.is_complex(X_complex):
        raise ValueError("X_complex must be complex-valued")

    B, F, T = X_complex.shape

    if M.ndim != 4 or M.shape[0] != B or M.shape[2] != F or M.shape[3] != T:
        raise ValueError(f"Unexpected M shape {M.shape}, expected (B,1,{F},{T})")

    # Remove channel dimension from M
    M = M[:, 0, :, :]  # (B, F, T)

    X_mag = X_complex.abs()
    X_phase = X_complex.angle()

    X_logmag = torch.log(X_mag + 1e-7)

    # bounded perturbation via tanh
    Y_logmag = X_logmag + eps * torch.tanh(M)

    Y_mag = torch.exp(Y_logmag)
    Y_complex = torch.polar(Y_mag, X_phase)  # same phase, modified magnitude
    return Y_complex


# ---------- High-level helper: waveform + bits -> watermarked waveform ----------

def encode_watermark_waveform(
    waveform: torch.Tensor,
    bits: torch.Tensor,
    encoder: WatermarkEncoder,
    eps: float,
    stft_cfg: STFTConfig,
) -> torch.Tensor:
    """
    Convenience wrapper for the full forward pass on a single waveform.

    waveform: (1, T) or (T,)
    bits: (n_bits,) or (1, n_bits)
    encoder: WatermarkEncoder
    eps: watermark strength
    stft_cfg: STFTConfig used for STFT/ISTFT

    returns:
        y: (1, T) watermarked waveform
    """
    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)  # (1, T)
    if waveform.ndim != 2 or waveform.shape[0] != 1:
        raise ValueError(f"Expected waveform (T,) or (1,T), got {waveform.shape}")

    if bits.ndim == 1:
        bits = bits.unsqueeze(0)  # (1, n_bits)
    elif bits.ndim != 2:
        raise ValueError(f"bits must be (n_bits,) or (B,n_bits), got {bits.shape}")

    # STFT
    X = stft(waveform, stft_cfg)  # (B=1, F, T_frames)

    # log|X| for encoder
    logmag = stft_logmag(waveform, stft_cfg)   # (B=1, F, T_frames)
    logmag = logmag.unsqueeze(1)               # (B, 1, F, T_frames)

    # mask
    M = encoder(logmag, bits)                  # (B, 1, F, T_frames)

    # apply mask
    Y = apply_watermark_mask(X, M, eps)        # (B, F, T_frames)

    # inverse STFT (use original length)
    y = istft(Y, stft_cfg, length=waveform.shape[-1])  # (1, T)

    return y
