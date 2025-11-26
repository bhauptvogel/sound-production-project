# watermarking/baseline.py

from dataclasses import dataclass, field
from typing import List, Tuple

import torch

from .stft_utils import STFTConfig, stft, istft


@dataclass
class BaselineConfig:
    """
    Simple fixed-band spectral watermark.

    - Uses STFT with a shared STFTConfig.
    - Chooses a contiguous band of frequency bins [low_bin, high_bin].
    - For each bit, uses a pair of bins (f0, f1) from that range.
    - Bit=1: boost f0, attenuate f1.
    - Bit=0: attenuate f0, boost f1.
    """

    stft_cfg: STFTConfig = field(default_factory=STFTConfig)
    low_bin: int = 40        # ~1.7 kHz if sr=44.1k, n_fft=1024
    high_bin: int = 200      # ~8.6 kHz
    alpha: float = 0.1       # strength of modification
    n_bits: int = 32         # payload length

    def _check_valid(self, n_freq: int) -> None:
        if self.low_bin < 0 or self.high_bin >= n_freq:
            raise ValueError(
                f"low_bin/high_bin ({self.low_bin}, {self.high_bin}) "
                f"must be within [0, {n_freq - 1}]"
            )
        if self.low_bin >= self.high_bin:
            raise ValueError("low_bin must be < high_bin")
        n_bins = self.high_bin - self.low_bin + 1
        if 2 * self.n_bits > n_bins:
            raise ValueError(
                f"Not enough bins for {self.n_bits} bits in range "
                f"[{self.low_bin}, {self.high_bin}] (only {n_bins} bins). "
                f"Need at least {2 * self.n_bits}."
            )

    def bin_pairs(self, n_freq: int) -> Tuple[List[int], List[int]]:
        """
        Returns two lists of bin indices (f0_list, f1_list), one pair per bit.
        """
        self._check_valid(n_freq)
        bins = list(range(self.low_bin, self.high_bin + 1))
        bins = bins[: 2 * self.n_bits]
        f0 = bins[0::2]
        f1 = bins[1::2]
        return f0, f1


def embed_baseline(
    waveform: torch.Tensor,
    bits: torch.Tensor,
    cfg: BaselineConfig,
) -> torch.Tensor:
    """
    Embed bits into waveform using fixed-band amplitude tweaks.

    waveform: (1, T) or (T,)
    bits: 1D tensor of 0/1, length cfg.n_bits
    returns: watermarked waveform, same shape as input (1, T)
    """
    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)  # (1, T)
    elif waveform.ndim != 2:
        raise ValueError(f"Expected waveform shape (T,) or (1,T), got {waveform.shape}")

    bits = bits.view(-1).to(torch.int64)
    if bits.numel() != cfg.n_bits:
        raise ValueError(
            f"bits length ({bits.numel()}) != cfg.n_bits ({cfg.n_bits}). "
            "Either adjust cfg.n_bits or pass the correct number of bits."
        )

    # Compute STFT
    X = stft(waveform, cfg.stft_cfg)  # (B, F, T_frames)
    B, F, T_frames = X.shape

    f0_list, f1_list = cfg.bin_pairs(F)
    X_mod = X.clone()

    # For each bit, boost/attenuate its pair
    for i, b in enumerate(bits):
        f0 = f0_list[i]
        f1 = f1_list[i]
        if int(b.item()) == 1:
            s0 = 1.0 + cfg.alpha
            s1 = 1.0 - cfg.alpha
        else:
            s0 = 1.0 - cfg.alpha
            s1 = 1.0 + cfg.alpha

        # scale complex STFT directly (changes magnitude, keeps phase)
        X_mod[:, f0, :] = X_mod[:, f0, :] * s0
        X_mod[:, f1, :] = X_mod[:, f1, :] * s1

    # Inverse STFT, preserve original length
    y = istft(X_mod, cfg.stft_cfg, length=waveform.shape[-1])  # (1, T)
    return y


def extract_baseline(
    waveform: torch.Tensor,
    cfg: BaselineConfig,
) -> torch.Tensor:
    """
    Recover bits from waveform using energy comparison in each bin pair.

    waveform: (1, T) or (T,)
    returns: bits_hat, shape (cfg.n_bits,) of dtype int64 with values 0/1
    """
    if waveform.ndim == 1:
        waveform = waveform.unsqueeze(0)
    elif waveform.ndim != 2:
        raise ValueError(f"Expected waveform shape (T,) or (1,T), got {waveform.shape}")

    X = stft(waveform, cfg.stft_cfg)  # (B, F, T_frames)
    B, F, T_frames = X.shape

    f0_list, f1_list = cfg.bin_pairs(F)
    bits_hat = []

    for f0, f1 in zip(f0_list, f1_list):
        # average magnitude across time (and batch)
        e0 = X[:, f0, :].abs().mean()
        e1 = X[:, f1, :].abs().mean()
        bit = 1 if e0 > e1 else 0
        bits_hat.append(bit)

    return torch.tensor(bits_hat, dtype=torch.int64)
