# evaluate_baseline.py

#!/usr/bin/env python

import argparse
import torch

from watermarking.data import load_audio, save_audio
from watermarking.baseline import BaselineConfig, embed_baseline, extract_baseline


def snr_db(x: torch.Tensor, y: torch.Tensor) -> float:
    """
    Signal-to-noise ratio between x and y in dB.
    """
    if x.ndim == 1:
        x = x.unsqueeze(0)
    if y.ndim == 1:
        y = y.unsqueeze(0)

    # align lengths
    T = min(x.shape[-1], y.shape[-1])
    x = x[..., :T]
    y = y[..., :T]

    noise = x - y
    p_signal = torch.mean(x**2)
    p_noise = torch.mean(noise**2) + 1e-12
    return float(10.0 * torch.log10(p_signal / p_noise))


def main():
    ap = argparse.ArgumentParser(description="Evaluate baseline watermark (SNR + BER)")
    ap.add_argument("--in", dest="inp", required=True, help="Input clean WAV")
    ap.add_argument("--out", dest="out", default="watermarked.wav")
    ap.add_argument("--bits", type=int, default=32, help="Number of bits to embed")
    ap.add_argument("--alpha", type=float, default=0.1, help="Embedding strength")
    ap.add_argument("--low-bin", type=int, default=40)
    ap.add_argument("--high-bin", type=int, default=200)
    ap.add_argument(
        "--noise-std",
        type=float,
        default=0.0,
        help="Optional Gaussian noise std applied before extraction",
    )
    args = ap.parse_args()

    x, sr = load_audio(args.inp, target_sr=44_100, mono=True, normalize="peak")

    bits = torch.randint(0, 2, (args.bits,), dtype=torch.int64)

    cfg = BaselineConfig(
        n_bits=args.bits,
        alpha=args.alpha,
        low_bin=args.low_bin,
        high_bin=args.high_bin,
    )

    # Embed
    y = embed_baseline(x, bits, cfg)

    # SNR of watermarking itself
    snr = snr_db(x, y)
    print(f"SNR (clean -> watermarked): {snr:.2f} dB")

    save_audio(args.out, y, sr, normalize="none")
    print(f"Saved watermarked audio to {args.out}")

    # Optional additive noise as a crude "attack"
    y_attack = y
    if args.noise_std > 0.0:
        noise = torch.randn_like(y_attack) * args.noise_std
        y_attack = y_attack + noise
        print(f"Applied Gaussian noise with std={args.noise_std}")

    # Extract
    bits_hat = extract_baseline(y_attack, cfg)

    bit_errors = int((bits != bits_hat).sum().item())
    ber = bit_errors / bits.numel()

    print("True bits:     ", "".join(str(int(b)) for b in bits))
    print("Recovered bits:", "".join(str(int(b)) for b in bits_hat))
    print(f"Bit errors: {bit_errors}/{bits.numel()}  BER = {ber:.4f}")


if __name__ == "__main__":
    main()
