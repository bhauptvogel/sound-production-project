# watermarking/losses.py

from dataclasses import dataclass
from typing import Sequence, Tuple

import torch
import torch.nn.functional as F

from .stft_utils import STFTConfig, stft


@dataclass
class SpectralLossConfig:
    stft_cfg: STFTConfig
    sample_rate: int = 44_100
    # frequency bands in Hz, and their weights
    bands: Tuple[Tuple[float, float], ...] = (
        (0.0, 400.0),      # lows
        (400.0, 4000.0),   # mids
        (4000.0, 8000.0),  # highs
    )
    band_weights: Tuple[float, ...] = (0.5, 1.0, 0.7)


def snr_db(x: torch.Tensor, y: torch.Tensor) -> float:
    """
    Signal-to-noise ratio between x and y in dB.
    """
    if x.ndim == 1:
        x = x.unsqueeze(0)
    if y.ndim == 1:
        y = y.unsqueeze(0)

    T = min(x.shape[-1], y.shape[-1])
    x = x[..., :T]
    y = y[..., :T]

    noise = x - y
    p_signal = torch.mean(x**2)
    p_noise = torch.mean(noise**2) + 1e-12
    return float(10.0 * torch.log10(p_signal / p_noise))


def log_spectral_distance_weighted(
    x: torch.Tensor,
    y: torch.Tensor,
    cfg: SpectralLossConfig,
) -> torch.Tensor:
    """
    Band-weighted log-spectral distance (LSD).

    x, y: (B,T) waveforms
    returns: scalar tensor
    """
    stft_cfg = cfg.stft_cfg

    if x.ndim == 1:
        x = x.unsqueeze(0)
    if y.ndim == 1:
        y = y.unsqueeze(0)

    X = stft(x, stft_cfg)  # (B,F,Tf)
    Y = stft(y, stft_cfg)  # (B,F,Tf)

    X_log = torch.log(X.abs() + 1e-7)
    Y_log = torch.log(Y.abs() + 1e-7)

    diff2 = (X_log - Y_log) ** 2  # (B,F,Tf)

    B, F, Tf = diff2.shape
    device = diff2.device

    # build frequency axis and band weights
    freqs = torch.linspace(
        0.0, cfg.sample_rate / 2.0, steps=F, device=device
    )  # (F,)

    weights = torch.zeros(F, device=device)
    for (f_lo, f_hi), w in zip(cfg.bands, cfg.band_weights):
        mask = (freqs >= f_lo) & (freqs < f_hi)
        weights[mask] = w
    # fallback weight 1.0 for unassigned (if any)
    weights[weights == 0.0] = 1.0

    weights = weights.view(1, F, 1)  # (1,F,1)

    weighted_diff2 = diff2 * weights
    lsd = weighted_diff2.mean()  # single scalar
    return lsd


def bit_loss_bce(
    logits: torch.Tensor,
    bits: torch.Tensor,
) -> torch.Tensor:
    """
    BCE-with-logits bit loss.

    logits: (B,n_bits)
    bits: (B,n_bits) in {0,1}
    """
    return F.binary_cross_entropy_with_logits(logits, bits)
