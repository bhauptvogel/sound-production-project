#!/usr/bin/env python
import argparse
import os
from pathlib import Path
from datasets import Dataset, Audio
from huggingface_hub import HfApi, login

def upload_clips(
    data_dir: str,
    repo_id: str,
    token: str = None,
    private: bool = False,
    num_proc: int = 4
):
    """
    Scans a directory for audio files, creates a Hugging Face Dataset, 
    and uploads it to the Hub.
    """
    data_path = Path(data_dir)
    if not data_path.exists():
        raise FileNotFoundError(f"Directory {data_dir} does not exist.")

    # Find all audio files
    extensions = {".wav", ".flac", ".ogg", ".mp3"}
    audio_files = [
        str(p) for p in sorted(data_path.rglob("*")) 
        if p.suffix.lower() in extensions
    ]
    
    if not audio_files:
        raise ValueError(f"No audio files found in {data_dir}")
        
    print(f"Found {len(audio_files)} audio files in {data_dir}")

    # Create dataset dictionary
    # We store the path. The cast_column('audio', Audio()) will handle loading.
    dataset_dict = {"audio": audio_files}
    
    ds = Dataset.from_dict(dataset_dict)
    
    # Cast the 'audio' column to the Audio feature so HF handles resampling/decoding if needed,
    # or just treats them as audio files.
    ds = ds.cast_column("audio", Audio())

    print("Dataset created locally. Pushing to Hugging Face Hub...")
    
    # Authenticate if token provided
    if token:
        login(token=token)
    
    # Push to hub
    ds.push_to_hub(
        repo_id, 
        private=private, 
        num_proc=num_proc
    )
    
    print(f"Successfully uploaded dataset to https://huggingface.co/datasets/{repo_id}")

def main():
    parser = argparse.ArgumentParser(description="Upload audio clips folder to Hugging Face Dataset")
    parser.add_argument("--data-dir", type=str, default="clips", help="Directory containing audio files")
    parser.add_argument("--repo-id", type=str, required=True, help="HF Repo ID (e.g. username/dataset-name)")
    parser.add_argument("--token", type=str, default=None, help="HF Access Token (optional if logged in)")
    parser.add_argument("--private", action="store_true", help="Make dataset private")
    parser.add_argument("--num-proc", type=int, default=4, help="Number of processes for uploading")
    
    args = parser.parse_args()
    
    upload_clips(
        data_dir=args.data_dir,
        repo_id=args.repo_id,
        token=args.token,
        private=args.private,
        num_proc=args.num_proc
    )

if __name__ == "__main__":
    main()

