# extract_cli.py

#!/usr/bin/env python

import argparse

from watermarking.data import load_audio
from watermarking.baseline import BaselineConfig, extract_baseline


def main():
    ap = argparse.ArgumentParser(description="Baseline spectral watermark extractor")
    ap.add_argument("--in", dest="inp", required=True, help="Input (watermarked) WAV")
    ap.add_argument(
        "--n-bits",
        type=int,
        required=True,
        help="Number of bits expected in the watermark",
    )
    ap.add_argument("--alpha", type=float, default=0.1, help="Embedding strength")
    ap.add_argument("--low-bin", type=int, default=40, help="Lower STFT bin index")
    ap.add_argument("--high-bin", type=int, default=200, help="Upper STFT bin index")
    args = ap.parse_args()

    wav, sr = load_audio(args.inp, target_sr=44_100, mono=True, normalize="peak")

    cfg = BaselineConfig(
        n_bits=args.n_bits,
        alpha=args.alpha,
        low_bin=args.low_bin,
        high_bin=args.high_bin,
    )

    bits_hat = extract_baseline(wav, cfg)
    bits_str = "".join(str(int(b)) for b in bits_hat)
    print("Recovered bits:", bits_str)


if __name__ == "__main__":
    main()
