# embed_cli.py

#!/usr/bin/env python

import argparse
import torch

from watermarking.data import load_audio, save_audio
from watermarking.baseline import BaselineConfig, embed_baseline


def parse_bits(bits_str: str) -> torch.Tensor:
    bits = []
    for ch in bits_str.strip():
        if ch not in ("0", "1"):
            raise ValueError("Bits string must contain only 0 and 1.")
        bits.append(int(ch))
    return torch.tensor(bits, dtype=torch.int64)


def main():
    ap = argparse.ArgumentParser(description="Baseline spectral watermark embedder")
    ap.add_argument("--in", dest="inp", required=True, help="Input WAV file")
    ap.add_argument("--out", dest="out", required=True, help="Output watermarked WAV")
    ap.add_argument(
        "--bits",
        dest="bits_str",
        help="Bit string like 010101. If omitted, random bits are used.",
        default=None,
    )
    ap.add_argument(
        "--n-bits",
        type=int,
        default=32,
        help="Number of random bits (if --bits is not provided)",
    )
    ap.add_argument("--alpha", type=float, default=0.1, help="Embedding strength")
    ap.add_argument("--low-bin", type=int, default=40, help="Lower STFT bin index")
    ap.add_argument("--high-bin", type=int, default=200, help="Upper STFT bin index")
    args = ap.parse_args()

    wav, sr = load_audio(args.inp, target_sr=44_100, mono=True, normalize="peak")

    if args.bits_str is not None:
        bits = parse_bits(args.bits_str)
    else:
        bits = torch.randint(0, 2, (args.n_bits,), dtype=torch.int64)

    cfg = BaselineConfig(
        n_bits=bits.numel(),
        alpha=args.alpha,
        low_bin=args.low_bin,
        high_bin=args.high_bin,
    )

    y = embed_baseline(wav, bits, cfg)
    save_audio(args.out, y, sr, normalize="none")

    bits_str = "".join(str(int(b)) for b in bits)
    print("Embedded bits:", bits_str)
    print(f"Saved watermarked audio to {args.out}")


if __name__ == "__main__":
    main()