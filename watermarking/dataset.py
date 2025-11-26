# watermarking/dataset.py

import pathlib
import random
from typing import List, Literal

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
        split: Literal["train", "val", "all"] = "all",
        val_fraction: float = 0.1,
        seed: int = 42,
    ):
        super().__init__()
        self.root_dir = pathlib.Path(root_dir)
        self.clip_duration = clip_duration
        self.target_sr = target_sr

        exts = {".wav", ".flac", ".ogg"}
        all_paths: List[pathlib.Path] = [
            p
            for p in sorted(self.root_dir.rglob("*"))
            if p.suffix.lower() in exts
        ]
        if not all_paths:
            raise RuntimeError(f"No audio files found in {self.root_dir}")

        # Deterministic split
        rng = random.Random(seed)
        rng.shuffle(all_paths)

        num_val = int(len(all_paths) * val_fraction)
        # Ensure at least one val sample if fraction > 0 and enough files exist
        if val_fraction > 0 and num_val == 0 and len(all_paths) > 1:
             num_val = 1

        if split == "train":
            self.paths = all_paths[num_val:]
        elif split == "val":
            self.paths = all_paths[:num_val]
        else:  # "all"
            self.paths = all_paths

        if not self.paths:
            if split == "val" and num_val == 0:
                print("Warning: Validation set is empty. Check val_fraction or dataset size.")
            else:
                raise RuntimeError(f"Dataset split '{split}' is empty.")

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
            start = random.randint(0, T - self.clip_len)
            wav = wav[start : start + self.clip_len]

        return wav  # (T,)
