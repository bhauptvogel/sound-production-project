import argparse
import torch

from watermarking.data import load_audio
from watermarking.stft_utils import (
    STFTConfig,
    MelConfig,
    stft_logmag,
    LogMelSpec,
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    args = ap.parse_args()

    wav, sr = load_audio(args.inp, target_sr=44_100, mono=True, normalize="peak")
    # wav: (1, T)
    wav = wav.squeeze(0)  # (T,)

    stft_cfg = STFTConfig(n_fft=1024, hop_length=256, win_length=1024)
    logmag = stft_logmag(wav, stft_cfg)
    print("logmag shape:", logmag.shape)  # (1, F, T_frames)

    mel_cfg = MelConfig(sample_rate=sr, n_fft=1024, hop_length=256, win_length=1024)
    logmel_extractor = LogMelSpec(mel_cfg)
    logmel = logmel_extractor(wav)
    print("logmel shape:", logmel.shape)  # (1, n_mels, T_frames)


if __name__ == "__main__":
    main()
