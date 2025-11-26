# evaluate_baseline.py

#!/usr/bin/env python

import argparse
import math
import random
from pathlib import Path
from typing import List, Optional, Tuple

import matplotlib.pyplot as plt
import torch
from tqdm import tqdm

from watermarking.data import load_audio, save_audio
from watermarking.baseline import BaselineConfig, embed_baseline, extract_baseline
from watermarking.dataset import RandomClipDataset


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


def evaluate_alpha(
    waveform: torch.Tensor,
    bits: torch.Tensor,
    cfg: BaselineConfig,
    noise_std: float,
) -> Tuple[torch.Tensor, float, float, int, torch.Tensor]:
    """
    Returns (watermarked_waveform, snr_db, ber, bit_errors, recovered_bits).
    """
    y = embed_baseline(waveform, bits, cfg)
    snr = snr_db(waveform, y)

    y_attack = y
    if noise_std > 0.0:
        noise = torch.randn_like(y_attack) * noise_std
        y_attack = y_attack + noise

    bits_hat = extract_baseline(y_attack, cfg)
    bit_errors = int((bits != bits_hat).sum().item())
    ber = bit_errors / bits.numel()
    return y, snr, ber, bit_errors, bits_hat


def format_out_paths(base_path: Path, alphas: List[float]) -> List[Path]:
    if len(alphas) == 1:
        return [base_path]

    suffix = base_path.suffix if base_path.suffix else ".wav"
    stem = base_path.stem
    parent = base_path.parent
    paths = []
    for alpha in alphas:
        alpha_label = str(alpha).replace(".", "p")
        paths.append(parent / f"{stem}_alpha{alpha_label}{suffix}")
    return paths


def main():
    ap = argparse.ArgumentParser(description="Evaluate baseline watermark (SNR + BER)")
    ap.add_argument("--in", dest="inp", help="Input clean WAV (single-file mode)")
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
    ap.add_argument(
        "--alpha-values",
        type=float,
        nargs="+",
        default=None,
        help="Sweep multiple alpha values (overrides --alpha)",
    )
    ap.add_argument(
        "--plot",
        default="baseline_alpha_sweep.png",
        help="Path to save the alpha sweep plot",
    )
    ap.add_argument(
        "--num-clips",
        type=int,
        default=100,
        help="Number of random dataset clips to evaluate (>=1)",
    )
    ap.add_argument(
        "--dataset-dir",
        default=None,
        help="Directory with audio files for multi-clip evaluation (defaults to 'clips')",
    )
    ap.add_argument(
        "--clip-duration",
        type=float,
        default=2.0,
        help="Clip duration in seconds when sampling from dataset",
    )
    args = ap.parse_args()

    alpha_values = args.alpha_values if args.alpha_values else [args.alpha]
    is_sweep = args.alpha_values is not None
    results = []

    use_dataset = args.num_clips > 1
    if args.num_clips < 1:
        raise ValueError("--num-clips must be >= 1")

    if use_dataset:
        dataset_dir = Path(args.dataset_dir) if args.dataset_dir else Path("clips")
        if not dataset_dir.exists():
            raise FileNotFoundError(
                f"Dataset directory {dataset_dir} does not exist."
            )
        dataset = RandomClipDataset(
            root_dir=dataset_dir,
            clip_duration=args.clip_duration,
            target_sr=44_100,
        )
        aggregated = {
            alpha: {
                "snr_sum": 0.0,
                "snr_count": 0,
                "snr_invalid": 0,
                "bit_errors": 0,
                "total_bits": 0,
            }
            for alpha in alpha_values
        }

        clip_iter = tqdm(range(args.num_clips), desc="Evaluating clips")
        for clip_idx in clip_iter:
            idx = random.randint(0, len(dataset) - 1)
            wav = dataset[idx].unsqueeze(0)  # (1, T)
            bits = torch.randint(0, 2, (args.bits,), dtype=torch.int64)

            for alpha in alpha_values:
                cfg = BaselineConfig(
                    n_bits=args.bits,
                    alpha=alpha,
                    low_bin=args.low_bin,
                    high_bin=args.high_bin,
                )
                _, snr, ber, bit_errors, _ = evaluate_alpha(
                    wav, bits, cfg, args.noise_std
                )
                stats = aggregated[alpha]
                if math.isfinite(snr):
                    stats["snr_sum"] += snr
                    stats["snr_count"] += 1
                else:
                    stats["snr_invalid"] += 1
                aggregated[alpha]["bit_errors"] += bit_errors
                aggregated[alpha]["total_bits"] += bits.numel()

        for alpha in alpha_values:
            stats = aggregated[alpha]
            avg_snr: Optional[float] = None
            if stats["snr_count"] > 0:
                avg_snr = stats["snr_sum"] / stats["snr_count"]
            total_bits = max(stats["total_bits"], 1)
            ber = stats["bit_errors"] / total_bits
            results.append(
                {
                    "alpha": alpha,
                    "snr": avg_snr,
                    "ber": ber,
                    "bit_errors": stats["bit_errors"],
                    "total_bits": total_bits,
                    "out_path": None,
                    "bits_hat": None,
                    "snr_invalid": stats["snr_invalid"],
                }
            )
    else:
        if not args.inp:
            raise ValueError("--in is required for single-file evaluation.")

        x, sr = load_audio(args.inp, target_sr=44_100, mono=True, normalize="peak")
        bits = torch.randint(0, 2, (args.bits,), dtype=torch.int64)
        out_paths = format_out_paths(Path(args.out), alpha_values)

        for alpha, out_path in zip(alpha_values, out_paths):
            cfg = BaselineConfig(
                n_bits=args.bits,
                alpha=alpha,
                low_bin=args.low_bin,
                high_bin=args.high_bin,
            )
            y, snr, ber, bit_errors, bits_hat = evaluate_alpha(
                x, bits, cfg, args.noise_std
            )
            save_audio(out_path, y, sr, normalize="none")
            snr_value: Optional[float] = snr if math.isfinite(snr) else None
            results.append(
                {
                    "alpha": alpha,
                    "snr": snr_value,
                    "ber": ber,
                    "bit_errors": bit_errors,
                    "total_bits": bits.numel(),
                    "out_path": out_path,
                    "bits_hat": bits_hat,
                    "snr_invalid": 0 if snr_value is not None else 1,
                }
            )

    if not use_dataset and len(alpha_values) == 1 and not is_sweep:
        res = results[0]
        if args.noise_std > 0.0:
            print(f"Applied Gaussian noise with std={args.noise_std}")
        if res["snr"] is not None:
            print(f"SNR (clean -> watermarked): {res['snr']:.2f} dB")
        else:
            print("SNR (clean -> watermarked): N/A (signal or noise is zero)")
        print(f"Saved watermarked audio to {res['out_path']}")
        print("True bits:     ", "".join(str(int(b)) for b in bits))
        print(
            "Recovered bits:",
            "".join(str(int(b)) for b in res["bits_hat"]),
        )
        print(f"Bit errors: {res['bit_errors']}/{bits.numel()}  BER = {res['ber']:.4f}")
        return

    if args.noise_std > 0.0:
        print(f"Applied Gaussian noise with std={args.noise_std}")
    print("Alpha sweep results:")
    for res in results:
        snr_str = f"{res['snr']:.2f} dB" if res["snr"] is not None else "N/A"
        line = (
            f" alpha={res['alpha']:.4f} | SNR={snr_str} | "
            f"BER={res['ber']:.4f}"
        )
        if res["out_path"]:
            line += f" | saved={res['out_path']}"
        if res.get("snr_invalid"):
            line += f" | invalid SNR samples={res['snr_invalid']}"
        print(line)

    fig, ax_snr = plt.subplots()
    alphas = [res["alpha"] for res in results]
    bers = [res["ber"] for res in results]

    ax_ber = ax_snr.twinx()
    valid_snr = [(res["alpha"], res["snr"]) for res in results if res["snr"] is not None]
    if valid_snr:
        snr_alphas, snr_values = zip(*valid_snr)
        ax_snr.plot(snr_alphas, snr_values, marker="o", color="tab:blue", label="SNR (dB)")
    ax_ber.plot(alphas, bers, marker="s", color="tab:red", label="BER")

    ax_snr.set_xlabel("alpha")
    ax_snr.set_ylabel("SNR (dB)", color="tab:blue")
    ax_ber.set_ylabel("BER (lower is better)", color="tab:red")
    ax_ber.invert_yaxis()
    ax_snr.grid(True, alpha=0.3)
    fig.tight_layout()

    plot_path = Path(args.plot)
    if plot_path.parent != Path(""):
        plot_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(plot_path, dpi=200)
    print(f"Saved alpha sweep plot to {plot_path}")


if __name__ == "__main__":
    main()
