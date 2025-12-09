#!/usr/bin/env python

import argparse
import json
import math
import os
import subprocess
import tempfile
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import torch.nn.functional as F
import numpy as np
from tqdm import tqdm
import soundfile as sf

from watermarking.models import (
    WatermarkEncoder,
    WatermarkDecoder,
    EncoderConfig,
    DecoderConfig,
    encode_watermark_waveform,
)
from watermarking.channel import (
    ChannelConfig,
    DifferentiableChannel,
    mp3_roundtrip,
    _ensure_batch,
)
from watermarking.stft_utils import STFTConfig, stft, stft_logmag
from watermarking.dataset import RandomClipDataset, HuggingFaceAudioDataset
from watermarking.losses import snr_db, log_spectral_distance_weighted, SpectralLossConfig
from watermarking.data import load_audio, save_audio


def aac_roundtrip(
    waveform: torch.Tensor,
    sr: int,
    bitrate_kbps: int = 128,
) -> torch.Tensor:
    """
    AAC encoding round-trip via ffmpeg.
    """
    batched, had_batch = _ensure_batch(waveform)
    device = batched.device
    dtype = batched.dtype
    B, T = batched.shape
    waveform_np = batched.detach().cpu().numpy()

    outs = []

    for b in range(B):
        with tempfile.TemporaryDirectory() as tmpdir:
            wav_path = os.path.join(tmpdir, "in.wav")
            aac_path = os.path.join(tmpdir, "out.m4a")
            wav2_path = os.path.join(tmpdir, "out.wav")

            sf.write(wav_path, waveform_np[b], sr)

            # encode
            try:
                subprocess.run(
                    [
                        "ffmpeg",
                        "-y",
                        "-loglevel",
                        "error",
                        "-i",
                        wav_path,
                        "-c:a",
                        "aac",
                        "-b:a",
                        f"{bitrate_kbps}k",
                        aac_path,
                    ],
                    check=True,
                )
                # decode
                subprocess.run(
                    ["ffmpeg", "-y", "-loglevel", "error", "-i", aac_path, wav2_path],
                    check=True,
                )
                y, _ = sf.read(wav2_path)
            except subprocess.CalledProcessError:
                # Fallback if ffmpeg fails (e.g. aac encoder issues)
                # return original with warning or zeros
                print(f"Warning: AAC roundtrip failed for batch item {b}")
                y = waveform_np[b]

            if y.ndim > 1:
                y = y.mean(axis=1)
            y_t = torch.from_numpy(y).float()

            # Crop/pad per item back to original length T
            if y_t.shape[0] < T:
                y_t = F.pad(y_t, (0, T - y_t.shape[0]))
            elif y_t.shape[0] > T:
                y_t = y_t[:T]

            outs.append(y_t)

    y_out = torch.stack(outs, dim=0).to(device=device, dtype=dtype)  # (B, T)
    if not had_batch:
        return y_out[0]
    return y_out


def load_models(
    encoder_ckpt: str,
    decoder_ckpt: str,
    n_bits: int,
    stft_cfg: STFTConfig,
    device: str,
) -> Tuple[WatermarkEncoder, WatermarkDecoder]:
    enc_cfg = EncoderConfig(
        n_bits=n_bits,
        stft_cfg=stft_cfg,
        base_channels=64,
        bit_emb_dim=32,
    )
    dec_cfg = DecoderConfig(
        n_bits=n_bits,
        stft_cfg=stft_cfg,
        base_channels=64,
    )

    encoder = WatermarkEncoder(enc_cfg).to(device)
    decoder = WatermarkDecoder(dec_cfg).to(device)

    if encoder_ckpt:
        print(f"Loading encoder from {encoder_ckpt}...")
        encoder.load_state_dict(torch.load(encoder_ckpt, map_location=device))
    else:
        print("Warning: No encoder checkpoint provided, using random weights.")

    if decoder_ckpt:
        print(f"Loading decoder from {decoder_ckpt}...")
        decoder.load_state_dict(torch.load(decoder_ckpt, map_location=device))
    else:
        print("Warning: No decoder checkpoint provided, using random weights.")

    encoder.eval()
    decoder.eval()
    return encoder, decoder


def decode_bits(
    decoder: WatermarkDecoder,
    waveform: torch.Tensor,
    stft_cfg: STFTConfig,
) -> torch.Tensor:
    """
    waveform: (B, T)
    returns: (B, n_bits) predicted bits (0 or 1)
    """
    with torch.no_grad():
        X_att = stft(waveform, stft_cfg)
        X_att_log = torch.log(X_att.abs() + 1e-7).unsqueeze(1)  # (B, 1, F, T)
        logits = decoder(X_att_log)
        probs = torch.sigmoid(logits)
        return (probs > 0.5).float()


def run_eval(args):
    device = torch.device(args.device)
    
    # Setup STFT
    stft_cfg = STFTConfig(
        n_fft=args.n_fft,
        hop_length=args.hop_length,
        win_length=args.win_length,
        center=True,
    )
    
    # Load models
    encoder, decoder = load_models(
        args.encoder_ckpt,
        args.decoder_ckpt,
        args.n_bits,
        stft_cfg,
        args.device,
    )
    
    # Setup Dataset
    # Check if local directory exists or fallback to HF
    use_hf = args.use_hf
    dataset = None
    
    # If eval_dir is provided, check if valid, else switch to HF
    if args.eval_dir:
        dataset_dir = Path(args.eval_dir)
        if not use_hf:
            if not dataset_dir.exists():
                print(f"Dataset directory {dataset_dir} does not exist. Switching to HF dataset.")
                use_hf = True
            elif not any(dataset_dir.rglob("*.wav")) and not any(dataset_dir.rglob("*.flac")) and not any(dataset_dir.rglob("*.ogg")):
                 print(f"Dataset directory {dataset_dir} contains no audio files. Switching to HF dataset.")
                 use_hf = True
    elif not args.input_file:
         # No input file and no eval dir -> try HF
         use_hf = True

    if use_hf:
        print("Using Hugging Face dataset: benmainbird/watermarking-clips")
        dataset = HuggingFaceAudioDataset(
            dataset_name="benmainbird/watermarking-clips",
            clip_duration=args.clip_duration,
            target_sr=args.sample_rate,
            split=args.split,
        )
    elif args.eval_dir:
        dataset = RandomClipDataset(
            root_dir=args.eval_dir,
            clip_duration=args.clip_duration,
            target_sr=args.sample_rate,
            split=args.split,
        )

    if dataset:
        # Use full dataset length unless num_clips is explicitly smaller
        dataset_len = len(dataset)
        if args.num_clips is not None and args.num_clips > 0 and args.num_clips < dataset_len:
            num_iters = args.num_clips
            print(f"Evaluating on {num_iters} clips (subset of {dataset_len} in '{args.split}' split)")
        else:
            num_iters = dataset_len
            print(f"Evaluating on {num_iters} clips (full '{args.split}' split)")

    elif args.input_file:
        # Single file mode
        print(f"Evaluating on single file: {args.input_file}")
        num_iters = 1
    else:
        # Should be covered by dataset loading logic, but just in case
        raise ValueError("Must provide either --eval-dir, --input-file, or allow HF dataset fallback")

    # Metrics setup
    spec_loss_cfg = SpectralLossConfig(stft_cfg=stft_cfg, sample_rate=args.sample_rate)

    # Define attacks to run
    # Each attack is a tuple: (name, function_that_takes_waveform_and_returns_attacked)
    attacks = []
    
    # 1. Identity (No Attack)
    attacks.append(("Identity", lambda w: w))
    
    # 2. Noise
    if args.test_noise:
        attacks.append(("Noise (std=0.01)", lambda w: w + torch.randn_like(w) * 0.01))
    
    # 3. Resampling
    if args.test_resample:
        # 0.9x speed
        from watermarking.channel import random_resample
        attacks.append(("Resample (0.9x)", lambda w: random_resample(w, 0.9, 0.9)))
        attacks.append(("Resample (1.1x)", lambda w: random_resample(w, 1.1, 1.1)))

    # 4. MP3
    if args.test_mp3:
        attacks.append(("MP3 (128k)", lambda w: mp3_roundtrip(w, args.sample_rate, 128)))
        attacks.append(("MP3 (64k)", lambda w: mp3_roundtrip(w, args.sample_rate, 64)))

    # 5. AAC
    if args.test_aac:
        attacks.append(("AAC (128k)", lambda w: aac_roundtrip(w, args.sample_rate, 128)))

    # 6. Quantization
    if args.test_quant:
        from watermarking.channel import quantize_ste
        attacks.append(("Quant (12-bit)", lambda w: quantize_ste(w, 12, 12)))
    
    # 7. EQ
    if args.test_eq:
        from watermarking.channel import random_eq_stft
        eq_cfg = ChannelConfig(stft_cfg=stft_cfg, eq_num_bands=6, eq_gain_db_min=-6, eq_gain_db_max=6)
        attacks.append(("Random EQ", lambda w: random_eq_stft(w, eq_cfg)))

    # Aggregate results
    results_agg = {
        name: {"ber_sum": 0.0, "snr_sum": 0.0, "lsd_sum": 0.0, "count": 0}
        for name, _ in attacks
    }

    single_file_results = []
    
    # Setup listening samples directory
    save_samples_dir = None
    if args.num_save_samples > 0:
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        save_samples_dir = Path("eval_samples") / timestamp
        save_samples_dir.mkdir(parents=True, exist_ok=True)
        print(f"Saving {args.num_save_samples} pairs of audio samples to {save_samples_dir}")

    # For single file, load it once
    wav_in_single = None
    if args.input_file:
        wav_in_single, _ = load_audio(args.input_file, target_sr=args.sample_rate, mono=True)
        wav_in_single = wav_in_single.unsqueeze(0).to(device) # (1, T)
    
    pbar = tqdm(range(num_iters), desc="Eval")
    
    samples_saved_count = 0

    for i in pbar:
        if dataset:
            # If we are iterating sequentially
            wav_in = dataset[i].unsqueeze(0).to(device) # (1, T)
        else:
            wav_in = wav_in_single
        
        # Generate bits
        bits = torch.randint(0, 2, (1, args.n_bits), device=device).float()
        
        # Encode
        with torch.no_grad():
            X = stft(wav_in, stft_cfg)
            logmag = torch.log(X.abs() + 1e-7).unsqueeze(1)
            M = encoder(logmag, bits)
            from watermarking.models import apply_watermark_mask
            from watermarking.stft_utils import istft
            Y_complex = apply_watermark_mask(X, M, args.eps)
            y_watermarked = istft(Y_complex, stft_cfg, length=wav_in.shape[-1])
            
            # Audio Metrics (Clean vs Watermarked)
            snr_val = snr_db(wav_in, y_watermarked)
            lsd_val = log_spectral_distance_weighted(wav_in, y_watermarked, spec_loss_cfg).item()
            
        # Save sample pairs if requested
        if save_samples_dir and samples_saved_count < args.num_save_samples:
            # Save original
            orig_path = save_samples_dir / f"sample{samples_saved_count}_original.wav"
            save_audio(orig_path, wav_in.squeeze(0), args.sample_rate)
            
            # Save watermarked (Identity attack basically)
            wm_path = save_samples_dir / f"sample{samples_saved_count}_watermarked.wav"
            save_audio(wm_path, y_watermarked.squeeze(0), args.sample_rate)
            
            # Write text file with info
            info_path = save_samples_dir / f"sample{samples_saved_count}_info.txt"
            with open(info_path, "w") as f:
                f.write(f"SNR: {snr_val:.2f} dB\n")
                f.write(f"LSD: {lsd_val:.4f}\n")
                f.write(f"Bits: {bits.cpu().int().tolist()}\n")
            
            samples_saved_count += 1

        # For each attack
        for atk_name, atk_fn in attacks:
            y_att = atk_fn(y_watermarked)
            
            # Decode
            bits_hat = decode_bits(decoder, y_att, stft_cfg)
            
            # BER
            bit_errors = (bits_hat != bits).sum().item()
            ber = bit_errors / args.n_bits
            
            agg = results_agg[atk_name]
            agg["ber_sum"] += ber
            agg["snr_sum"] += snr_val 
            agg["lsd_sum"] += lsd_val
            agg["count"] += 1
            
            if args.input_file:
                single_file_results.append({
                    "attack": atk_name,
                    "ber": ber,
                    "snr": snr_val,
                    "lsd": lsd_val,
                    "recovered_bits": bits_hat.cpu().int().numpy().tolist()[0],
                    "original_bits": bits.cpu().int().numpy().tolist()[0]
                })
                
                if args.save_audio:
                    out_name = Path(args.output_dir) / f"watermarked_{atk_name.replace(' ', '_').replace('(', '').replace(')', '')}.wav"
                    save_audio(out_name, y_att.squeeze(0).cpu(), args.sample_rate)

    # Print Summary
    print("\n" + "="*60)
    print(f"{'Attack Type':<20} | {'BER':<10} | {'SNR (dB)':<10} | {'LSD':<10}")
    print("-" * 60)
    
    final_stats = {}
    
    for name, agg in results_agg.items():
        count = max(agg["count"], 1)
        avg_ber = agg["ber_sum"] / count
        avg_snr = agg["snr_sum"] / count
        avg_lsd = agg["lsd_sum"] / count
        
        print(f"{name:<20} | {avg_ber:.4f}     | {avg_snr:.2f}       | {avg_lsd:.4f}")
        
        final_stats[name] = {
            "ber": avg_ber,
            "snr": avg_snr,
            "lsd": avg_lsd
        }

    print("="*60)
    
    # Save stats
    if args.output_json:
        # Ensure any special float values (NaN, Inf) are handled
        def safe_json_float(val):
            if math.isnan(val):
                return None
            if math.isinf(val):
                return "Infinity" if val > 0 else "-Infinity"
            return val

        # Convert aggregation for JSON safety
        json_stats = {}
        for name, stats in final_stats.items():
            json_stats[name] = {
                "ber": safe_json_float(stats["ber"]),
                "snr": safe_json_float(stats["snr"]),
                "lsd": safe_json_float(stats["lsd"])
            }

        with open(args.output_json, 'w') as f:
            json.dump(json_stats, f, indent=2)
        print(f"Saved results to {args.output_json}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate Neural Watermarking Model")
    
    # Model inputs
    parser.add_argument("--encoder-ckpt", type=str, required=True, help="Path to encoder checkpoint")
    parser.add_argument("--decoder-ckpt", type=str, required=True, help="Path to decoder checkpoint")
    parser.add_argument("--n-bits", type=int, default=32, help="Number of bits")
    parser.add_argument("--eps", type=float, default=0.02, help="Watermark strength")
    
    # Data
    parser.add_argument("--eval-dir", type=str, default=None, help="Directory of clips to evaluate")
    parser.add_argument("--split", type=str, default="val", choices=["train", "val", "all"], help="Dataset split to use")
    parser.add_argument("--input-file", type=str, default=None, help="Single file to evaluate")
    
    # Optional: limit number of clips evaluated (useful for debugging, default: evaluate all)
    parser.add_argument("--num-clips", type=int, default=None, help="Limit number of clips to evaluate (default: all in split)")
    
    parser.add_argument("--clip-duration", type=float, default=2.0, help="Clip duration (s)")
    parser.add_argument("--sample-rate", type=int, default=44100)
    parser.add_argument("--num-save-samples", type=int, default=5, help="Number of original/watermarked pairs to save for listening")
    
    # STFT
    parser.add_argument("--n-fft", type=int, default=1024)
    parser.add_argument("--hop-length", type=int, default=256)
    parser.add_argument("--win-length", type=int, default=1024)
    
    # Attack flags
    parser.add_argument("--test-noise", action="store_true", help="Test Gaussian noise")
    parser.add_argument("--test-resample", action="store_true", help="Test resampling")
    parser.add_argument("--test-mp3", action="store_true", help="Test MP3 compression")
    parser.add_argument("--test-aac", action="store_true", help="Test AAC compression")
    parser.add_argument("--test-quant", action="store_true", help="Test quantization")
    parser.add_argument("--test-eq", action="store_true", help="Test random EQ")
    parser.add_argument("--test-all", action="store_true", help="Enable all attacks")
    
    # Output
    parser.add_argument("--output-dir", type=str, default="eval_results", help="Dir to save audio/plots")
    parser.add_argument("--output-json", type=str, default="eval_results.json", help="JSON file for metrics")
    parser.add_argument("--save-audio", action="store_true", help="Save watermarked audio (single file mode)")
    parser.add_argument("--device", type=str, default="cuda" if torch.cuda.is_available() else "cpu")
    
    # New flag for HF
    parser.add_argument("--use-hf", action="store_true", help="Force use of Hugging Face dataset")
    
    args = parser.parse_args()
    
    if args.test_all:
        args.test_noise = True
        args.test_resample = True
        args.test_mp3 = True
        args.test_aac = True
        args.test_quant = True
        args.test_eq = True
        
    Path(args.output_dir).mkdir(parents=True, exist_ok=True)
    
    run_eval(args)


if __name__ == "__main__":
    main()
