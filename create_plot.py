import re
import matplotlib.pyplot as plt

log_path = "results/20251126-175025_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep10_chnone.txt"

epoch_idx = []
bit_loss = []
ber = []
snr = []

# Regex for epoch summary lines
pattern = re.compile(
    r"\[Epoch\s+(\d+)\]\s+Enc\s+([0-9.]+)\s+\|\s+Dec\s+([0-9.]+)\s+\|\s+Bit\s+([0-9.]+)\s+\|"
    r"\s+L2\s+([0-9.]+)\s+\|\s+LSD\s+([0-9.]+)\s+\|\s+BER\s+([0-9.]+)\s+\|\s+SNR\s+([0-9.]+)\s+dB"
)

with open(log_path, "r") as f:
    for line in f:
        m = pattern.search(line)
        if m:
            epoch_idx.append(int(m.group(1)))
            # Enc / Dec / Bit are equal in this run, we use Bit as "loss"
            bit_loss.append(float(m.group(4)))
            ber.append(float(m.group(7)))
            snr.append(float(m.group(8)))

print("Epochs:", epoch_idx)
print("Bit loss:", bit_loss)
print("BER:", ber)
print("SNR:", snr)

fig, axes = plt.subplots(3, 1, figsize=(6, 8), sharex=True)

axes[0].plot(epoch_idx, bit_loss)
axes[0].set_ylabel("Bit loss")
axes[0].grid(True, linestyle=":")

axes[1].plot(epoch_idx, ber)
axes[1].set_ylabel("BER")
axes[1].grid(True, linestyle=":")

axes[2].plot(epoch_idx, snr)
axes[2].set_xlabel("Epoch")
axes[2].set_ylabel("SNR [dB]")
axes[2].grid(True, linestyle=":")

# fig.suptitle("Neural watermarking training (16 bits, $\\varepsilon = 0.2$)")
fig.tight_layout()
plt.savefig("plots/neural_training_metrics_bits16_eps0.2.png", dpi=200)

