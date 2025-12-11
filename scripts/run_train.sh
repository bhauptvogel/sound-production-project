#!/usr/bin/env bash
# cd /home/bmainbird/UL/sound-production/project && source venv/bin/activate
# cd /workspace/sound-production-project

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Move HF cache to workspace to avoid disk quota issues on home dir
export HF_HOME="$(pwd)/hf_cache"
export HF_DATASETS_CACHE="${HF_HOME}/datasets"
mkdir -p "${HF_DATASETS_CACHE}"

# Force HF to look in workspace for cache
export XDG_CACHE_HOME="$(pwd)/hf_cache"

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

# Default configuration
DATA_DIR="clips/"
EPOCHS=20
BATCH=32
NUM_BITS=16
EPS=0.3
ALPHA=0.2
BETA=0.2
MASK_REG=1e-4
LOGIT_REG=1e-4
DECODER_LR=1e-4
DECODER_STEPS=1
SAVE_PT=1 # 1 = save checkpoints, 0 = don't save
CHANNEL_MODE="noise_only" # default stage
USE_HF=1 # 0 = auto-detect, 1 = force HF
# MAX_STEPS=500

# Parse arguments
while [ $# -gt 0 ]; do
  case "$1" in
    --data-dir=*)
      DATA_DIR="${1#*=}"
      ;;
    --epochs=*)
      EPOCHS="${1#*=}"
      ;;
    --batch-size=*)
      BATCH="${1#*=}"
      ;;
    --n-bits=*)
      NUM_BITS="${1#*=}"
      ;;
    --eps=*)
      EPS="${1#*=}"
      ;;
    --alpha-l2=*)
      ALPHA="${1#*=}"
      ;;
    --beta-lsd=*)
      BETA="${1#*=}"
      ;;
    --mask-reg=*)
      MASK_REG="${1#*=}"
      ;;
    --logit-reg=*)
      LOGIT_REG="${1#*=}"
      ;;
    --decoder-lr=*)
      DECODER_LR="${1#*=}"
      ;;
    --decoder-steps=*)
      DECODER_STEPS="${1#*=}"
      ;;
    --save-pt=*)
      SAVE_PT="${1#*=}"
      ;;
    --channel-mode=*)
      CHANNEL_MODE="${1#*=}"
      ;;
    --use-hf=*)
      USE_HF="${1#*=}"
      ;;
    --use-hf)
      USE_HF=1
      ;;
    *)
      echo "Unknown argument: $1"
      exit 1
      ;;
  esac
  shift
done

run_stage() {
  local channel_mode="$1"

  mkdir -p checkpoints plots results
  RUN_TAG=$(printf "bits%s_eps%s_alpha%s_beta%s_mask%s_logit%s_decLR%s_decSteps%s_bs%s_ep%s_ch%s_hf%s" \
    "${NUM_BITS}" "${EPS}" "${ALPHA}" "${BETA}" "${MASK_REG}" "${LOGIT_REG}" \
    "${DECODER_LR}" "${DECODER_STEPS}" "${BATCH}" "${EPOCHS}" "${channel_mode}" "${USE_HF}")
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
use-hf          = ${USE_HF}
============================================================
EOF

  CMD=(
      python -m watermarking.train 
      --data-dir "${DATA_DIR}" 
      --epochs "${EPOCHS}" 
      --batch-size "${BATCH}" 
      --n-bits "${NUM_BITS}" 
      --eps "${EPS}" 
      --alpha-l2 "${ALPHA}" 
      --beta-lsd "${BETA}" 
      --mask-reg "${MASK_REG}" 
      --logit-reg "${LOGIT_REG}" 
      --decoder-lr "${DECODER_LR}" 
      --decoder-steps "${DECODER_STEPS}" 
      --channel-mode "${channel_mode}" 
      --plot-path "${PLOT_PATH}" 
      --encoder-ckpt "${ENC_CKPT}" 
      --decoder-ckpt "${DEC_CKPT}" 
      --save-pt "${SAVE_PT}" 
      --lr "${DECODER_LR}"
  )
  
  if [ "${USE_HF}" -eq 1 ]; then
      CMD+=(--use-hf)
  fi

  TMP_LOG=$(mktemp)
  "${CMD[@]}" | tee "${TMP_LOG}"
  cat "${TMP_LOG}" >> "${LOG_FILE}"
  rm -f "${TMP_LOG}"
    # --max-steps-per-epoch "${MAX_STEPS}"
}

# Run experiment with configured (or default) channel mode
run_stage "${CHANNEL_MODE}"
