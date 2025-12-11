#!/bin/bash
set -e

# Configuration
# DATA_DIR="clips"
CHECKPOINT_DIR="checkpoints"  # Adjust if your checkpoints are elsewhere


# Move HF cache to workspace to avoid disk quota issues on home dir
export HF_HOME="$(pwd)/hf_cache"
export HF_DATASETS_CACHE="${HF_HOME}/datasets"
mkdir -p "${HF_DATASETS_CACHE}"

# Force HF to look in workspace for cache
export XDG_CACHE_HOME="$(pwd)/hf_cache"

# Function to run evaluation for a specific pair of checkpoints
run_evaluation_for_pair() {
    local ENC_CKPT="$1"
    local DEC_CKPT="$2"

    if [ -z "$ENC_CKPT" ] || [ -z "$DEC_CKPT" ]; then
        echo "Error: Missing checkpoints for evaluation."
        return 1
    fi

    # Derive Output Directory name from Encoder filename
    local ENC_BASENAME=$(basename "$ENC_CKPT")
    local ENC_STAMP=${ENC_BASENAME%_encoder.pt}
    local OUTPUT_DIR="results/eval_${ENC_STAMP}"

    # Check if results already exist
    if [ -f "$OUTPUT_DIR/metrics.json" ]; then
        echo "Evaluation results already exist at: $OUTPUT_DIR/metrics.json"
        echo "Skipping evaluation for $ENC_STAMP"
        return 0
    fi

    echo "---------------------------------------------------"
    echo "Starting evaluation for: $ENC_STAMP"
    echo "Using Encoder: $ENC_CKPT"
    echo "Using Decoder: $DEC_CKPT"
    echo "Output Directory: $OUTPUT_DIR"

    # Extract parameters from filename if possible
    # Default values
    local N_BITS=32
    local EPS=0.02

    # Attempt to parse bits
    # Use basename to avoid directory confusing regex if it contained "bits" string
    local CKPT_NAME=$(basename "$ENC_CKPT")
    
    if [[ $CKPT_NAME =~ bits([0-9]+) ]]; then
        N_BITS=${BASH_REMATCH[1]}
    fi
    echo "Detected n-bits from filename: $N_BITS"

    # Attempt to parse eps
    if [[ $CKPT_NAME =~ eps([0-9.]+) ]]; then
        EPS=${BASH_REMATCH[1]}
    fi
    echo "Detected eps from filename: $EPS"

    # Create output directory
    mkdir -p "$OUTPUT_DIR"

    # Run Evaluation
    # Using the virtual environment python
    venv/bin/python -m watermarking.eval \
        --encoder-ckpt "$ENC_CKPT" \
        --decoder-ckpt "$DEC_CKPT" \
        --split "val" \
        --use-hf \
        --n-bits "$N_BITS" \
        --eps "$EPS" \
        --test-all \
        --num-save-samples 5 \
        --output-dir "$OUTPUT_DIR" \
        --output-json "$OUTPUT_DIR/metrics.json"

    echo "Evaluation complete for $ENC_STAMP"
    echo "---------------------------------------------------"
}

# Argument handling
ARG1="$1"

if [ "$ARG1" == "--all" ]; then
    # 0. Run all missing evaluations
    echo "Running evaluation for all checkpoints in $CHECKPOINT_DIR..."
    
    # Iterate over all encoder checkpoints
    for ENC_CKPT in ${CHECKPOINT_DIR}/*_encoder.pt; do
        # Infer corresponding decoder checkpoint
        # Replace _encoder.pt with _decoder.pt
        DEC_CKPT="${ENC_CKPT%_encoder.pt}_decoder.pt"
        
        if [ -f "$DEC_CKPT" ]; then
            run_evaluation_for_pair "$ENC_CKPT" "$DEC_CKPT"
        else
            echo "Warning: No matching decoder found for $ENC_CKPT. Skipping."
        fi
    done
    
    # Generate the site once after all are done
    ./scripts/generate_site.py
    exit 0

elif [ -z "$ARG1" ]; then
    # 1. No arguments: Find the latest checkpoints
    echo "No arguments provided. Searching for latest checkpoints in $CHECKPOINT_DIR..."
    LATEST_ENC=$(ls ${CHECKPOINT_DIR}/*_encoder.pt 2>/dev/null | sort -r | head -n1)
    LATEST_DEC=$(ls ${CHECKPOINT_DIR}/*_decoder.pt 2>/dev/null | sort -r | head -n1)
    
    run_evaluation_for_pair "$LATEST_ENC" "$LATEST_DEC"
    ./scripts/generate_site.py

elif [ -f "$ARG1" ]; then
    # 2. Argument is a file path: Assume explicit encoder and decoder paths provided
    ENC_CKPT="$1"
    DEC_CKPT="$2"
    if [ -z "$DEC_CKPT" ]; then
        echo "Error: If providing an encoder file path, you must also provide the decoder file path."
        exit 1
    fi
    run_evaluation_for_pair "$ENC_CKPT" "$DEC_CKPT"
    ./scripts/generate_site.py

else
    # 3. Argument is a timestamp prefix: Find matching checkpoints
    TIMESTAMP="$1"
    echo "Searching for checkpoints matching timestamp: $TIMESTAMP"
    
    # Find files starting with the timestamp
    LATEST_ENC=$(ls ${CHECKPOINT_DIR}/${TIMESTAMP}*_encoder.pt 2>/dev/null | head -n1)
    LATEST_DEC=$(ls ${CHECKPOINT_DIR}/${TIMESTAMP}*_decoder.pt 2>/dev/null | head -n1)
    
    if [ -z "$LATEST_ENC" ] || [ -z "$LATEST_DEC" ]; then
        echo "Error: Could not find matching encoder/decoder checkpoints for timestamp $TIMESTAMP."
        exit 1
    fi

    run_evaluation_for_pair "$LATEST_ENC" "$LATEST_DEC"
    ./scripts/generate_site.py
fi
