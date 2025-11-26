# watermarking/dataset.py

import pathlib
from typing import List, Tuple

import torch
from torch.utils.data import Dataset

from .data import load_audio


class RandomClipDataset(Dataset):
    """
    Loads WAV/FLAC files from a directory and returns random mono clips
    of fixed duration.

    Each __getitem__ picks one file (round-robin) and a random offset.
    """

    def __init__(
        self,
        root_dir: str | pathlib.Path,
        clip_duration: float,
        target_sr: int = 44_100,
    ):
        super().__init__()
        self.root_dir = pathlib.Path(root_dir)
        self.clip_duration = clip_duration
        self.target_sr = target_sr

        exts = {".wav", ".flac", ".ogg"}
        self.paths: List[pathlib.Path] = [
            p
            for p in sorted(self.root_dir.rglob("*"))
            if p.suffix.lower() in exts
        ]
        if not self.paths:
            raise RuntimeError(f"No audio files found in {self.root_dir}")

        self.clip_len = int(self.target_sr * self.clip_duration)

    def __len__(self) -> int:
        # One virtual sample per source file; each access still uses a random crop.
        return len(self.paths)

    def __getitem__(self, idx: int) -> torch.Tensor:
        # pick file deterministically but offset/randomized
        path = self.paths[idx % len(self.paths)]
        wav, sr = load_audio(path, target_sr=self.target_sr, mono=True, normalize="peak")
        wav = wav.squeeze(0)  # (T,)

        T = wav.shape[-1]
        if T <= self.clip_len:
            # loop-pad if necessary
            reps = (self.clip_len + T - 1) // T
            wav = wav.repeat(reps)[: self.clip_len]
        else:
            # random crop
            import random

            start = random.randint(0, T - self.clip_len)
            wav = wav[start : start + self.clip_len]

        return wav  # (T,)
