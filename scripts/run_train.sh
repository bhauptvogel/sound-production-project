#!/usr/bin/env bash
# cd /home/bmainbird/UL/sound-production/project && source venv/bin/activate
git pull
cd /workspace/project
source venv/bin/activate

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
STAGE0_DATA_DIR="clips/"
STAGE0_EPOCHS=5
STAGE0_BATCH=32
STAGE0_BITS=16
STAGE0_EPS=0.025
STAGE0_ALPHA=0.01
STAGE0_BETA=0.01
STAGE0_MASK_REG=0.05
STAGE0_LOGIT_REG=0.001
STAGE0_DECODER_LR=5e-5
STAGE0_DECODER_STEPS=2
STAGE0_CHANNEL="none" # Stage 0: none, Stage 1: noise_only, Stage 3: full
# STAGE0_MAX_STEPS=500

mkdir -p checkpoints plots
RUN_TAG=$(printf "eps%s_mask%s_decLR%s_ch%s" "${STAGE0_EPS}" "${STAGE0_MASK_REG}" "${STAGE0_DECODER_LR}" "${STAGE0_CHANNEL}")
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
RUN_NAME="${RUN_TAG}_${TIMESTAMP}"
PLOT_PATH="plots/${RUN_NAME}.png"
ENC_CKPT="checkpoints/${RUN_NAME}_encoder.pt"
DEC_CKPT="checkpoints/${RUN_NAME}_decoder.pt"

cat <<EOF
============================================================
Stage 0 Configuration
------------------------------------------------------------
run-name        = ${RUN_NAME}
data-dir        = ${STAGE0_DATA_DIR}
epochs          = ${STAGE0_EPOCHS}
batch-size      = ${STAGE0_BATCH}
n-bits          = ${STAGE0_BITS}
eps             = ${STAGE0_EPS}
alpha-l2        = ${STAGE0_ALPHA}
beta-lsd        = ${STAGE0_BETA}
mask-reg        = ${STAGE0_MASK_REG}
logit-reg       = ${STAGE0_LOGIT_REG}
decoder-lr      = ${STAGE0_DECODER_LR}
decoder-steps   = ${STAGE0_DECODER_STEPS}
channel-mode    = ${STAGE0_CHANNEL}
max-steps-epoch = ${STAGE0_MAX_STEPS:-None}
plot-path       = ${PLOT_PATH}
enc-checkpoint  = ${ENC_CKPT}
dec-checkpoint  = ${DEC_CKPT}
============================================================
EOF

python -m watermarking.train \
  --data-dir "${STAGE0_DATA_DIR}" \
  --epochs "${STAGE0_EPOCHS}" \
  --batch-size "${STAGE0_BATCH}" \
  --n-bits "${STAGE0_BITS}" \
  --eps "${STAGE0_EPS}" \
  --alpha-l2 "${STAGE0_ALPHA}" \
  --beta-lsd "${STAGE0_BETA}" \
  --mask-reg "${STAGE0_MASK_REG}" \
  --logit-reg "${STAGE0_LOGIT_REG}" \
  --decoder-lr "${STAGE0_DECODER_LR}" \
  --decoder-steps "${STAGE0_DECODER_STEPS}" \
  --channel-mode "${STAGE0_CHANNEL}" \
  --plot-path "${PLOT_PATH}" \
  --encoder-ckpt "${ENC_CKPT}" \
  --decoder-ckpt "${DEC_CKPT}"
  # --max-steps-per-epoch "${STAGE0_MAX_STEPS}"
