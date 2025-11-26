# Neural Audio Watermarking

This repository implements a neural audio watermarking system based on a learnable encoder–decoder operating in the STFT domain, plus a differentiable channel that simulates realistic audio distortions. It is developed as part of the “Computer-Based Sound Production” lab project.

The main goal is to embed a short bitstring into mono audio such that:
- The watermark is **robust** to common transformations (noise, EQ, resampling, quantization).
- The **audio quality** remains high (good SNR, low spectral distortion).
- The system can be trained end-to-end on real audio clips.

---

## Repository structure

- `watermarking/models.py`  
  Neural encoder and decoder:
  - **Encoder**: takes log-magnitude STFT and a bit vector, outputs a mask over STFT bins that encodes the bits via frequency-pair templates plus a CNN residual.  
  - **Decoder**: CNN that reads log-magnitude STFT of (possibly attacked) audio and predicts bit logits.   

- `watermarking/stft_utils.py`  
  STFT/ISTFT helpers and log-magnitude features. :contentReference[oaicite:1]{index=1}  

- `watermarking/channel.py`  
  Differentiable channel that composes several attacks:
  - additive noise
  - random multi-band EQ in STFT domain
  - resampling / time-stretch
  - bit-depth quantization via straight-through estimator  
  Channel behaviour is controlled by a `ChannelConfig` and a `mode` flag (`none`, `noise_only`, `full`).   

- `watermarking/dataset.py`  
  `RandomClipDataset` that loads WAV/FLAC/OGG from a directory and returns random mono clips of fixed duration for training. :contentReference[oaicite:3]{index=3}  

- `watermarking/losses.py`  
  - Bit loss (`BCEWithLogits`)  
  - Band-weighted log spectral distance (LSD)  
  - SNR metric in dB :contentReference[oaicite:4]{index=4}  

- `watermarking/train.py`  
  Training script and `TrainingConfig` (CLI wrapper around it). Sets up dataset, encoder/decoder, channel, and optimizer, and runs training while tracking encoder loss, decoder loss, BER and SNR.   

- `run_train.sh`  
  Convenience script with a staged training schedule (starting from identity channel, then adding noise, then full channel).

---

## Installation

Create a virtual environment and install dependencies (PyTorch, torchaudio and basics like numpy, soundfile, tqdm):

```bash
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
# Example (adapt to your environment / CUDA version):
pip install torch torchaudio soundfile numpy tqdm
```
