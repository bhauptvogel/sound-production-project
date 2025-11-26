#!/usr/bin/env bash
cd /home/bmainbird/UL/sound-production/project && source venv/bin/activate 

# ============================================================================
# STAGED TRAINING APPROACH
# ============================================================================
# Start with Stage 0 to verify the model can learn, then gradually increase
# difficulty. See comments below for each stage.
#
# Stage 0: No channel attacks, bit loss only
#   - Verify encoder/decoder can learn basic watermarking
#   - Expected: bit loss ↓, BER ↓ (<0.1 ideally)
#
# Stage 1: Mild noise only, still bit loss only
#   - Add small amount of noise to test robustness
#   - Expected: BER slightly worse than Stage 0 but still learnable
#
# Stage 2: Add audio quality losses
#   - Re-enable L2 and LSD losses with small weights
#   - Expected: SNR stays >25-30 dB while BER continues to drop
#
# Stage 3: Full channel attacks
#   - All attacks enabled (noise, EQ, resample, quantize)
#   - Expected: Model learns to survive realistic distortions
# ============================================================================

# Stage 0 experiment: longer run on identity channel with stronger regularization
python -m watermarking.train \
  --data-dir clips/ \
  --epochs 5 \
  --batch-size 4 \
  --n-bits 16 \
  --eps 0.025 \
  --alpha-l2 0.01 \
  --beta-lsd 0.01 \
  --mask-reg 0.05 \
  --logit-reg 0.001 \
  --decoder-lr 5e-5 \
  --decoder-steps 2 \
  --channel-mode none
  # --max-steps-per-epoch 500

# Stage 1 experiment: mild noise channel after decoder stabilizes
# python -m watermarking.train \
#   --data-dir clips/ \
#   --epochs 2 \
#   --batch-size 4 \
#   --n-bits 16 \
#   --eps 0.02 \
#   --alpha-l2 0.02 \
#   --beta-lsd 0.02 \
#   --mask-reg 0.05 \
#   --logit-reg 0.001 \
#   --decoder-lr 5e-5 \
#   --decoder-steps 2 \
#   --channel-mode noise_only \
#   --max-steps-per-epoch 500

# Uncomment below to try Stage 3 (full channel):
# python -m watermarking.train \
#   --data-dir clips/ \
#   --epochs 5 \
#   --batch-size 4 \
#   --n-bits 16 \
#   --eps 0.015 \
#   --alpha-l2 0.05 \
#   --beta-lsd 0.05 \
#   --mask-reg 0.05 \
#   --logit-reg 0.002 \
#   --decoder-lr 5e-5 \
#   --decoder-steps 2 \
#   --channel-mode full \
#   --max-steps-per-epoch 1000

