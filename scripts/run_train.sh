#!/usr/bin/env bash
# cd /home/bmainbird/UL/sound-production/project && source venv/bin/activate
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

# Shared experiment configuration
DATA_DIR="clips/"
EPOCHS=10
BATCH=32
NUM_BITS=16
EPS=0.3
ALPHA=0.0
BETA=0.0
MASK_REG=0.0
LOGIT_REG=0.0
DECODER_LR=3e-4
DECODER_STEPS=0
SAVE_PT=1 # 1 = save checkpoints, 0 = don't save
# MAX_STEPS=500

run_stage() {
  local channel_mode="$1"

  mkdir -p checkpoints plots results
  RUN_TAG=$(printf "bits%s_eps%s_alpha%s_beta%s_mask%s_logit%s_decLR%s_decSteps%s_bs%s_ep%s_ch%s" \
    "${NUM_BITS}" "${EPS}" "${ALPHA}" "${BETA}" "${MASK_REG}" "${LOGIT_REG}" \
    "${DECODER_LR}" "${DECODER_STEPS}" "${BATCH}" "${EPOCHS}" "${channel_mode}")
  TIMESTAMP=$(date +%Y%m%d-%H%M%S)
  RUN_NAME="${TIMESTAMP}_${RUN_TAG}"
  PLOT_PATH="plots/${RUN_NAME}.png"
  ENC_CKPT="checkpoints/${RUN_NAME}_encoder.pt"
  DEC_CKPT="checkpoints/${RUN_NAME}_decoder.pt"
  LOG_FILE="results/${RUN_NAME}.txt"

  cat <<EOF
============================================================
Configuration
------------------------------------------------------------
run-name        = ${RUN_NAME}
data-dir        = ${DATA_DIR}
epochs          = ${EPOCHS}
batch-size      = ${BATCH}
n-bits          = ${NUM_BITS}
eps             = ${EPS}
alpha-l2        = ${ALPHA}
beta-lsd        = ${BETA}
mask-reg        = ${MASK_REG}
logit-reg       = ${LOGIT_REG}
decoder-lr      = ${DECODER_LR}
decoder-steps   = ${DECODER_STEPS}
channel-mode    = ${channel_mode}
max-steps-epoch = ${MAX_STEPS:-None}
plot-path       = ${PLOT_PATH}
enc-checkpoint  = ${ENC_CKPT}
dec-checkpoint  = ${DEC_CKPT}
save-pt         = ${SAVE_PT}
log-file        = ${LOG_FILE}
============================================================
EOF

  TMP_LOG=$(mktemp)
  python -m watermarking.train \
    --data-dir "${DATA_DIR}" \
    --epochs "${EPOCHS}" \
    --batch-size "${BATCH}" \
    --n-bits "${NUM_BITS}" \
    --eps "${EPS}" \
    --alpha-l2 "${ALPHA}" \
    --beta-lsd "${BETA}" \
    --mask-reg "${MASK_REG}" \
    --logit-reg "${LOGIT_REG}" \
    --decoder-lr "${DECODER_LR}" \
    --decoder-steps "${DECODER_STEPS}" \
    --channel-mode "${channel_mode}" \
    --plot-path "${PLOT_PATH}" \
    --encoder-ckpt "${ENC_CKPT}" \
    --decoder-ckpt "${DEC_CKPT}" \
    --save-pt "${SAVE_PT}" \
    --lr "${DECODER_LR}" | tee "${TMP_LOG}"
  cat "${TMP_LOG}" >> "${LOG_FILE}"
  rm -f "${TMP_LOG}"
    # --max-steps-per-epoch "${MAX_STEPS}"
}

# Run Stage 0 (identity channel). For Stage 1/3, call run_stage with noise_only/full.
run_stage "none"
