import argparse

import torch

from watermarking.data import load_audio, save_audio
from watermarking.stft_utils import STFTConfig, stft, istft


def snr_db(x: torch.Tensor, y: torch.Tensor) -> float:
    """
    Signal-to-noise ratio in dB between x and y.
    """
    # ensure same shape
    min_len = min(x.shape[-1], y.shape[-1])
    x = x[..., :min_len]
    y = y[..., :min_len]

    noise = x - y
    p_signal = torch.mean(x**2)
    p_noise = torch.mean(noise**2) + 1e-12
    return 10.0 * torch.log10(p_signal / p_noise)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", dest="out", default="stft_roundtrip.wav")
    args = ap.parse_args()

    wav, sr = load_audio(args.inp, target_sr=44_100, mono=True, normalize="peak")
    # wav: (1, T)
    cfg = STFTConfig(n_fft=1024, hop_length=256, win_length=1024, center=True)

    T = wav.shape[-1]

    X = stft(wav, cfg)              # (1, F, T_frames)
    wav_rec = istft(X, cfg, length=T) 

    # Align lengths (iSTFT can differ by a few samples if center=True)
    T = wav.shape[-1]
    wav_rec = wav_rec[..., :T]

    # Compute SNR
    snr = snr_db(wav, wav_rec)
    max_abs_diff = (wav - wav_rec).abs().max().item()

    print(f"SNR: {snr:.2f} dB")
    print(f"Max abs diff: {max_abs_diff:.6f}")

    save_audio(args.out, wav_rec, sr, normalize="none")
    print(f"Saved reconstructed audio to {args.out}")


if __name__ == "__main__":
    main()
