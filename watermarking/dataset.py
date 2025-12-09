# watermarking/dataset.py

import pathlib
import random
from typing import List, Literal, Optional

import torch
from torch.utils.data import Dataset
import numpy as np

from .data import load_audio

try:
    from datasets import load_dataset, Audio
except ImportError:
    load_dataset = None


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
            # We don't raise error immediately if we plan to fallback, 
            # but this class expects files. 
            # Ideally the caller checks existence before instantiating.
            pass

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

        if not self.paths and all_paths:
            if split == "val" and num_val == 0:
                print("Warning: Validation set is empty. Check val_fraction or dataset size.")
            else:
                # Only raise if files were found but split is empty
                raise RuntimeError(f"Dataset split '{split}' is empty.")
        elif not all_paths:
             # Caller should handle empty dir if they want
             self.paths = []

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


class HuggingFaceAudioDataset(Dataset):
    """
    Loads audio clips from a Hugging Face dataset.
    Falls back to this if local clips/ is missing.
    """

    def __init__(
        self,
        dataset_name: str,
        clip_duration: float,
        target_sr: int = 44_100,
        split: Literal["train", "val", "all"] = "all",
        val_fraction: float = 0.1,
        seed: int = 42,
        token: Optional[str] = None,
    ):
        super().__init__()
        if load_dataset is None:
            raise ImportError("Please install 'datasets' to use HuggingFaceAudioDataset: pip install datasets")

        self.dataset_name = dataset_name
        self.clip_duration = clip_duration
        self.target_sr = target_sr
        self.clip_len = int(self.target_sr * self.clip_duration)

        print(f"Loading HF dataset '{dataset_name}' (split='train' base)...")
        # Load the dataset (usually they have a train split by default)
        try:
            ds = load_dataset(dataset_name, split="train", token=token)
        except Exception as e:
             # Fallback if no train split
             ds = load_dataset(dataset_name, split=None, token=token)
             if isinstance(ds, dict):
                 # take first split available
                 ds = next(iter(ds.values()))
        
        # Configure resampling
        ds = ds.cast_column("audio", Audio(sampling_rate=target_sr))
        
        # Deterministic split via indices
        total_len = len(ds)
        indices = list(range(total_len))
        rng = random.Random(seed)
        rng.shuffle(indices)

        num_val = int(total_len * val_fraction)
        if val_fraction > 0 and num_val == 0 and total_len > 1:
            num_val = 1

        if split == "train":
            self.indices = indices[num_val:]
        elif split == "val":
            self.indices = indices[:num_val]
        else:
            self.indices = indices

        self.ds = ds
        print(f"Loaded HF dataset with {len(self.indices)} samples for split '{split}'")

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, idx: int) -> torch.Tensor:
        real_idx = self.indices[idx]
        item = self.ds[real_idx]
        
        # Item has {'audio': {'array': ..., 'sampling_rate': ...}, ...}
        audio_data = item["audio"]
        wav_np = audio_data["array"]
        
        # Ensure tensor
        wav = torch.from_numpy(wav_np).float()
        
        # Ensure mono
        if wav.ndim > 1:
            # If (C, T), mix to mono
            wav = wav.mean(dim=0)
        
        # Normalize (peak) - crucial for consistency with local load_audio
        max_val = wav.abs().max()
        if max_val > 1e-9:
            wav = wav / max_val

        T = wav.shape[-1]
        if T <= self.clip_len:
            # loop-pad
            if T == 0:
                 return torch.zeros(self.clip_len)
            reps = (self.clip_len + T - 1) // T
            wav = wav.repeat(reps)[: self.clip_len]
        else:
            # random crop
            start = random.randint(0, T - self.clip_len)
            wav = wav[start : start + self.clip_len]

        return wav
