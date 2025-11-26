import pathlib
from typing import Tuple, Literal, Optional

import numpy as np
import soundfile as sf
import torch
import torchaudio


NormalizationMode = Literal["none", "peak", "rms"]


def _to_mono(waveform: np.ndarray) -> np.ndarray:
    """
    waveform: (T,) or (T, C) or (C, T)
    returns: (T,) mono
    """
    if waveform.ndim == 1:
        return waveform

    if waveform.ndim != 2:
        raise ValueError(f"Unexpected waveform shape: {waveform.shape}")

    # Try to detect which axis represents channels (<=8 is a decent heuristic)
    channels_first = waveform.shape[0] <= 8 and waveform.shape[0] <= waveform.shape[1]
    channels_last = waveform.shape[1] <= 8 and waveform.shape[1] <= waveform.shape[0]

    if channels_last and not channels_first:
        # Typical soundfile output (T, C) where C <= 8
        waveform = waveform.T  # -> (C, T)
    elif not channels_first and not channels_last:
        # Ambiguous multi-channel shape; assume channels are along axis 0 if it is smaller
        if waveform.shape[0] > waveform.shape[1]:
            waveform = waveform.T

    if waveform.shape[0] > waveform.shape[1]:
        # After all heuristics we still expect (C, T) with C <= T
        waveform = waveform.T

    return waveform.mean(axis=0)


def _normalize_peak(x: torch.Tensor, peak: float = 0.99) -> torch.Tensor:
    max_abs = x.abs().max()
    if max_abs > 0:
        x = x * (peak / max_abs)
    return x


def _normalize_rms(x: torch.Tensor, target_rms: float = 0.1) -> torch.Tensor:
    rms = torch.sqrt(torch.mean(x**2) + 1e-8)
    if rms > 0:
        x = x * (target_rms / rms)
    return x


def load_audio(
    path: str | pathlib.Path,
    target_sr: int = 44_100,
    mono: bool = True,
    normalize: NormalizationMode = "peak",
) -> Tuple[torch.Tensor, int]:
    """
    Load audio as float32 torch tensor in range roughly [-1, 1].

    Returns:
        waveform: (1, T) tensor
        sr: int
    """
    path = pathlib.Path(path)
    data, sr = sf.read(path, always_2d=False)

    # to mono if requested
    if mono:
        data = _to_mono(data)

    # ensure float32
    if data.dtype != np.float32:
        data = data.astype(np.float32)

    # shape (T,) -> (1, T)
    if data.ndim == 1:
        data = data[None, :]
    elif data.ndim == 2:
        # assume (C, T); if not, user will hear it eventually – but for mono=True we already averaged
        if mono:
            data = data[None, :]
        else:
            data = data.T  # (T, C) -> (C, T)
    else:
        raise ValueError(f"Unexpected audio shape after sf.read: {data.shape}")

    wav = torch.from_numpy(data)  # (C, T)

    # resample if needed
    if sr != target_sr:
        wav = torchaudio.functional.resample(wav, orig_freq=sr, new_freq=target_sr)
        sr = target_sr

    # normalization
    if normalize == "peak":
        wav = _normalize_peak(wav)
    elif normalize == "rms":
        wav = _normalize_rms(wav)
    elif normalize == "none":
        pass
    else:
        raise ValueError(f"Unknown normalize mode: {normalize}")

    return wav, sr


def save_audio(
    path: str | pathlib.Path,
    waveform: torch.Tensor,
    sr: int,
    normalize: Optional[NormalizationMode] = None,
) -> None:
    """
    Save mono/stereo waveform to disk.

    waveform: (C, T) or (1, T) or (T,)
    """
    path = pathlib.Path(path)

    if isinstance(waveform, np.ndarray):
        wav = torch.from_numpy(waveform)
    else:
        wav = waveform

    # ensure 2D (C, T)
    if wav.ndim == 1:
        wav = wav.unsqueeze(0)
    elif wav.ndim != 2:
        raise ValueError(f"Unexpected waveform shape: {wav.shape}")

    wav = wav.detach().cpu().float()

    # optional re-normalization on output
    if normalize is not None and normalize != "none":
        if normalize == "peak":
            wav = _normalize_peak(wav)
        elif normalize == "rms":
            wav = _normalize_rms(wav)
        else:
            raise ValueError(f"Unknown normalization mode: {normalize}")

    # clamp to [-1, 1] for safety
    wav = torch.clamp(wav, -1.0, 1.0)

    # (C, T) -> (T, C) for soundfile
    wav_np = wav.T.numpy()
    sf.write(path, wav_np, sr)
