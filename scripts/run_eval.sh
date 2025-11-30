#!/bin/bash
set -e

# Configuration
DATA_DIR="clips"
CHECKPOINT_DIR="checkpoints"  # Adjust if your checkpoints are elsewhere

# Argument handling
ARG1="$1"

if [ -z "$ARG1" ]; then
    # 1. No arguments: Find the latest checkpoints
    echo "No arguments provided. Searching for latest checkpoints in $CHECKPOINT_DIR..."
    LATEST_ENC=$(ls ${CHECKPOINT_DIR}/*_encoder.pt 2>/dev/null | sort -r | head -n1)
    LATEST_DEC=$(ls ${CHECKPOINT_DIR}/*_decoder.pt 2>/dev/null | sort -r | head -n1)

elif [ -f "$ARG1" ]; then
    # 2. Argument is a file path: Assume explicit encoder and decoder paths provided
    ENC_CKPT="$1"
    DEC_CKPT="$2"
    if [ -z "$DEC_CKPT" ]; then
        echo "Error: If providing an encoder file path, you must also provide the decoder file path."
        exit 1
    fi
    LATEST_ENC="$ENC_CKPT"
    LATEST_DEC="$DEC_CKPT"
    echo "Using explicitly provided checkpoints."

else
    # 3. Argument is a timestamp prefix: Find matching checkpoints
    TIMESTAMP="$1"
    echo "Searching for checkpoints matching timestamp: $TIMESTAMP"
    
    # Find files starting with the timestamp
    LATEST_ENC=$(ls ${CHECKPOINT_DIR}/${TIMESTAMP}*_encoder.pt 2>/dev/null | head -n1)
    LATEST_DEC=$(ls ${CHECKPOINT_DIR}/${TIMESTAMP}*_decoder.pt 2>/dev/null | head -n1)
fi

if [ -z "$LATEST_ENC" ] || [ -z "$LATEST_DEC" ]; then
    echo "Error: Could not find matching encoder/decoder checkpoints."
    echo "Usage:"
    echo "  ./scripts/run_eval.sh                                     # Auto-detect latest"
    echo "  ./scripts/run_eval.sh 20251127-092954                     # By timestamp prefix"
    echo "  ./scripts/run_eval.sh path/to/encoder.pt path/to/decoder.pt  # Explicit paths"
    exit 1
fi

# Derive Output Directory name from Encoder filename
# Remove directory path
ENC_BASENAME=$(basename "$LATEST_ENC")
# Remove suffix "_encoder.pt"
ENC_STAMP=${ENC_BASENAME%_encoder.pt}
OUTPUT_DIR="results/eval_${ENC_STAMP}"

# Check if results already exist
if [ -f "$OUTPUT_DIR/metrics.json" ]; then
    echo "Evaluation results already exist at: $OUTPUT_DIR/metrics.json"
    echo "Skipping evaluation."
    exit 0
fi

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

# Update the results table
./scripts/create_results_table.py

echo "Evaluation complete! Results saved to $OUTPUT_DIR"
