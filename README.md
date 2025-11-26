# Neural Audio Watermarking

This repository implements a neural audio watermarking system based on a learnable encoder–decoder operating in the STFT domain, plus a differentiable channel that simulates realistic audio distortions. It is developed as part of the “Computer-Based Sound Production” lab project.

The main goal is to embed a short bitstring into mono audio such that:
- The watermark is **robust** to common transformations (noise, EQ, resampling, quantization).
- The **audio quality** remains high (good SNR, low spectral distortion).
- The system can be trained end-to-end on real audio clips.
