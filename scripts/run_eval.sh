#!/bin/bash
set -e

# Configuration
DATA_DIR="clips"
CHECKPOINT_DIR="checkpoints"  # Adjust if your checkpoints are elsewhere

# Find latest checkpoints (or specify manually)
# This assumes checkpoints are named like "encoder_epochX.pt"
# You might need to adjust this logic depending on how you save/name them
LATEST_ENC=$(ls -t ${CHECKPOINT_DIR}/*_encoder.pt 2>/dev/null | head -n1)
LATEST_DEC=$(ls -t ${CHECKPOINT_DIR}/*_decoder.pt 2>/dev/null | head -n1)

if [ -z "$LATEST_ENC" ] || [ -z "$LATEST_DEC" ]; then
    echo "Error: Could not find encoder/decoder checkpoints in $CHECKPOINT_DIR"
    echo "Please specify checkpoints manually or check the path."
    exit 1
fi

# Derive Output Directory name from Encoder filename
# Remove directory path
ENC_BASENAME=$(basename "$LATEST_ENC")
# Remove suffix "_encoder.pt"
ENC_STAMP=${ENC_BASENAME%_encoder.pt}
OUTPUT_DIR="results/eval_${ENC_STAMP}"

echo "Using Encoder: $LATEST_ENC"
echo "Using Decoder: $LATEST_DEC"
echo "Output Directory: $OUTPUT_DIR"

# Extract parameters from filename if possible
# Example filename: 20251126-234814_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR5e-4_decSteps0_bs32_ep10_chnone_encoder.pt
# We try to extract "bits16" -> 16 and "eps0.2" -> 0.2

# Default values
N_BITS=32
EPS=0.02

# Attempt to parse bits
if [[ $LATEST_ENC =~ bits([0-9]+) ]]; then
    N_BITS=${BASH_REMATCH[1]}
    echo "Detected n-bits from filename: $N_BITS"
fi

# Attempt to parse eps
if [[ $LATEST_ENC =~ eps([0-9.]+) ]]; then
    EPS=${BASH_REMATCH[1]}
    echo "Detected eps from filename: $EPS"
fi


# Create output directory
mkdir -p "$OUTPUT_DIR"

# Run Evaluation
# Using the virtual environment python
venv/bin/python -m watermarking.eval \
    --encoder-ckpt "$LATEST_ENC" \
    --decoder-ckpt "$LATEST_DEC" \
    --eval-dir "$DATA_DIR" \
    --split "val" \
    --n-bits "$N_BITS" \
    --eps "$EPS" \
    --test-all \
    --num-save-samples 5 \
    --output-dir "$OUTPUT_DIR" \
    --output-json "$OUTPUT_DIR/metrics.json"

echo "Evaluation complete! Results saved to $OUTPUT_DIR"
