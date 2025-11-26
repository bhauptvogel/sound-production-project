# train.py

#!/usr/bin/env python

import argparse
from dataclasses import dataclass
from tqdm.auto import tqdm

import torch
from torch.utils.data import DataLoader

from watermarking.stft_utils import STFTConfig
from watermarking.models import (
    EncoderConfig,
    DecoderConfig,
    WatermarkEncoder,
    WatermarkDecoder,
    apply_watermark_mask,
)
from watermarking.channel import ChannelConfig, DifferentiableChannel
from watermarking.dataset import RandomClipDataset
from watermarking.losses import (
    SpectralLossConfig,
    bit_loss_bce,
    log_spectral_distance_weighted,
    snr_db,
)
from watermarking.stft_utils import stft, istft


@dataclass
class TrainingConfig:
    data_dir: str
    sample_rate: int = 44_100
    clip_duration: float = 2.0

    batch_size: int = 8
    num_epochs: int = 10
    lr: float = 1e-4
    device: str = "cuda" if torch.cuda.is_available() else "cpu"
    max_steps_per_epoch: int | None = None  # None = use full dataset

    # watermark payload + strength
    n_bits: int = 32
    eps: float = 0.02  # watermark magnitude in log domain

    # loss weights
    alpha_l2: float = 0.1
    beta_lsd: float = 0.1

    # channel mode: "none", "noise_only", or "full"
    channel_mode: str = "full"

    decoder_steps: int = 1
    mask_reg: float = 0.0
    decoder_lr: float = 1e-4
    logit_reg: float = 0.0

    # STFT
    n_fft: int = 1024
    hop_length: int = 256
    win_length: int = 1024

    def __post_init__(self):
        if self.decoder_steps < 1:
            raise ValueError("decoder_steps must be >= 1")


def train(cfg: TrainingConfig):
    device = torch.device(cfg.device)

    # Dataset + loader
    dataset = RandomClipDataset(
        root_dir=cfg.data_dir,
        clip_duration=cfg.clip_duration,
        target_sr=cfg.sample_rate,
    )
    loader = DataLoader(
        dataset,
        batch_size=cfg.batch_size,
        shuffle=True,
        num_workers=4,
        drop_last=True,
    )

    # STFT config
    stft_cfg = STFTConfig(
        n_fft=cfg.n_fft,
        hop_length=cfg.hop_length,
        win_length=cfg.win_length,
        center=True,
    )

    # Models
    enc_cfg = EncoderConfig(
        n_bits=cfg.n_bits,
        stft_cfg=stft_cfg,
        base_channels=64,
        bit_emb_dim=32,
    )
    dec_cfg = DecoderConfig(
        n_bits=cfg.n_bits,
        stft_cfg=stft_cfg,
        base_channels=64,
    )

    encoder = WatermarkEncoder(enc_cfg).to(device)
    decoder = WatermarkDecoder(dec_cfg).to(device)

    # Differentiable channel
    ch_cfg = ChannelConfig(stft_cfg=stft_cfg, mode=cfg.channel_mode)
    channel = DifferentiableChannel(ch_cfg).to(device)

    # Spectral loss config
    spec_cfg = SpectralLossConfig(
        stft_cfg=stft_cfg,
        sample_rate=cfg.sample_rate,
    )

    # Optimizers
    enc_opt = torch.optim.Adam(encoder.parameters(), lr=cfg.lr)
    dec_opt = torch.optim.Adam(decoder.parameters(), lr=cfg.decoder_lr)

    print(f"Training on {cfg.device} with {len(dataset)} virtual samples.")

    for epoch in range(1, cfg.num_epochs + 1):
        encoder.train()
        decoder.train()
        channel.train()

        running_enc_loss = 0.0
        running_dec_loss = 0.0
        running_bit_loss = 0.0
        running_l2 = 0.0
        running_lsd = 0.0
        running_ber = 0.0
        running_snr = 0.0

        progress = tqdm(
            loader,
            desc=f"Epoch {epoch}/{cfg.num_epochs}",
            leave=True,
        )

        for step, batch in enumerate(progress, start=1):
            # Early stopping for debugging
            if cfg.max_steps_per_epoch is not None and step > cfg.max_steps_per_epoch:
                break
                
            x = batch.to(device)       # (B,T)
            B, T = x.shape

            bits = torch.randint(0, 2, (B, cfg.n_bits), device=device).float()
            X = stft(x, stft_cfg)
            # CRITICAL: We need to compute logmag from X, but X should be part of the graph
            # However, X comes from x (dataset), so it's fine. The key is that M depends on X_log
            # and Y depends on both X and M, so gradients should flow.
            X_log = torch.log(X.abs() + 1e-7)
            logmag_in = X_log.unsqueeze(1)

            M = encoder(logmag_in, bits)
            Y = apply_watermark_mask(X, M, eps=cfg.eps)
            y = istft(Y, stft_cfg, length=T)
            y_attacked = channel(y)

            X_att = stft(y_attacked, stft_cfg)
            X_att_log = torch.log(X_att.abs() + 1e-7).unsqueeze(1)

            # Decoder adaptation step(s)
            decoder_loss_total = 0.0
            for _ in range(cfg.decoder_steps):
                dec_opt.zero_grad()
                logits_dec = decoder(X_att_log.detach())
                decoder_loss = bit_loss_bce(logits_dec, bits)
                decoder_loss.backward()
                dec_opt.step()
                decoder_loss_total += decoder_loss.item()

            decoder_loss_val = decoder_loss_total / cfg.decoder_steps

            for p in decoder.parameters():
                p.requires_grad_(False)

            try:
                logits = decoder(X_att_log)
                bit_loss = bit_loss_bce(logits, bits)
            finally:
                for p in decoder.parameters():
                    p.requires_grad_(True)

            # Debugging: print statistics every 100 steps
            if step % 100 == 0:
                with torch.no_grad():
                    mask_stats = {
                        'mask_mean': M.mean().item(),
                        'mask_std': M.std().item(),
                        'mask_max': M.max().item(),
                        'mask_min': M.min().item(),
                        'tanh_mask_mean': torch.tanh(M).mean().item(),
                        'tanh_mask_std': torch.tanh(M).std().item(),
                    }
                    logit_stats = {
                        'logit_mean': logits.mean().item(),
                        'logit_std': logits.std().item(),
                        'logit_max': logits.max().item(),
                        'logit_min': logits.min().item(),
                    }
                    # Check if encoder produces different masks for different bits
                    # (sample two different bit patterns and compare masks)
                    if step == 100:
                        bits1 = torch.zeros(1, cfg.n_bits, device=device)
                        bits2 = torch.ones(1, cfg.n_bits, device=device)
                        M1 = encoder(logmag_in[:1], bits1)
                        M2 = encoder(logmag_in[:1], bits2)
                        mask_diff = (M1 - M2).abs().mean().item()
                        
                        # Also check if bit embedding itself is different
                        with torch.no_grad():
                            bit_emb1 = encoder.bit_mlp(bits1)
                            bit_emb2 = encoder.bit_mlp(bits2)
                            bit_emb_diff = (bit_emb1 - bit_emb2).abs().mean().item()
                        
                        print(f"\n[Debug step {step}] Bit embedding difference (all-0 vs all-1): {bit_emb_diff:.6f}")
                        print(f"[Debug step {step}] Mask difference (all-0 vs all-1 bits): {mask_diff:.6f}")
                        print(f"[Debug step {step}] Mask stats: {mask_stats}")
                        print(f"[Debug step {step}] Logit stats: {logit_stats}")
                        
            audio_l2 = torch.mean((y_attacked - x) ** 2)
            lsd = log_spectral_distance_weighted(x, y_attacked, spec_cfg)
            mask_penalty = cfg.mask_reg * torch.mean(torch.tanh(M) ** 2)  # keeps perturbations bounded
            logit_penalty = cfg.logit_reg * torch.mean(logits ** 2)
            loss = (
                bit_loss
                + cfg.alpha_l2 * audio_l2
                + cfg.beta_lsd * lsd
                + mask_penalty
                + logit_penalty
            )

            enc_opt.zero_grad()
            loss.backward()
            enc_opt.step()

            with torch.no_grad():
                probs = torch.sigmoid(logits)
                b_hat = (probs > 0.5).float()
                bit_errors = (b_hat != bits).sum().item()
                ber = bit_errors / (B * cfg.n_bits)
                batch_snr = snr_db(x.detach().cpu(), y_attacked.detach().cpu())

            running_enc_loss += loss.item()
            running_dec_loss += decoder_loss_val
            running_bit_loss += bit_loss.item()
            running_l2 += audio_l2.item()
            running_lsd += float(lsd.item())
            running_ber += ber
            running_snr += batch_snr

            n = step
            progress.set_postfix(
                enc=running_enc_loss / n,
                dec=running_dec_loss / n,
                bit=running_bit_loss / n,
                l2=running_l2 / n,
                lsd=running_lsd / n,
                ber=running_ber / n,
                snr=f"{running_snr / n:.1f}dB",
            )

        n = step
        print(
            f"[Epoch {epoch}] "
            f"Enc {running_enc_loss/n:.4f} | "
            f"Dec {running_dec_loss/n:.4f} | "
            f"Bit {running_bit_loss/n:.4f} | "
            f"L2 {running_l2/n:.4f} | "
            f"LSD {running_lsd/n:.4f} | "
            f"BER {running_ber/n:.4f} | "
            f"SNR {running_snr/n:.2f} dB"
        )

        # TODO: save encoder/decoder checkpoints here if you want


def parse_args() -> TrainingConfig:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", required=True, help="Directory with WAV/FLAC files")
    ap.add_argument("--epochs", type=int, default=10)
    ap.add_argument("--batch-size", type=int, default=8)
    ap.add_argument("--n-bits", type=int, default=32)
    ap.add_argument("--eps", type=float, default=0.02)
    ap.add_argument("--alpha-l2", type=float, default=0.1)
    ap.add_argument("--beta-lsd", type=float, default=0.1)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--device", type=str, default=None)
    ap.add_argument("--max-steps-per-epoch", type=int, default=None,
                    help="Limit steps per epoch for debugging (None = full dataset)")
    ap.add_argument("--channel-mode", type=str, default="full",
                    choices=["none", "noise_only", "full"],
                    help="Channel attack mode: 'none' (identity), 'noise_only', or 'full'")
    ap.add_argument("--decoder-steps", type=int, default=1,
                    help="Number of decoder update steps per batch")
    ap.add_argument("--mask-reg", type=float, default=0.0,
                    help="Weight for mask energy regularization term")
    ap.add_argument("--decoder-lr", type=float, default=1e-4,
                    help="Learning rate for decoder optimizer")
    ap.add_argument("--logit-reg", type=float, default=0.0,
                    help="Weight for decoder logit L2 penalty")
    args = ap.parse_args()

    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")

    return TrainingConfig(
        data_dir=args.data_dir,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        n_bits=args.n_bits,
        eps=args.eps,
        alpha_l2=args.alpha_l2,
        beta_lsd=args.beta_lsd,
        lr=args.lr,
        device=device,
        max_steps_per_epoch=args.max_steps_per_epoch,
        channel_mode=args.channel_mode,
        decoder_steps=args.decoder_steps,
        mask_reg=args.mask_reg,
        decoder_lr=args.decoder_lr,
        logit_reg=args.logit_reg,
    )


if __name__ == "__main__":
    cfg = parse_args()
    train(cfg)
