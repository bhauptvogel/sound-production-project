window.resultsData = [
  {
    "Date": "20251210",
    "Time": "151800",
    "bits": 16,
    "eps": 0.2,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.1,
    "logit_reg": 0.01,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "noise_only_hf1",
    "run_name": "20251210-151800_bits16_eps0.2_alpha0.0_beta0.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251210-151800_bits16_eps0.2_alpha0.0_beta0.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1.png",
    "eval_exists": false,
    "metrics": {}
  },
  {
    "Date": "20251210",
    "Time": "150024",
    "bits": 16,
    "eps": 0.2,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.1,
    "logit_reg": 0.01,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "noise_only_hf1",
    "run_name": "20251210-150024_bits16_eps0.2_alpha0.0_beta0.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1",
    "enc_checkpoint": false,
    "dec_checkpoint": false,
    "plot_url": null,
    "eval_exists": false,
    "metrics": {}
  },
  {
    "Date": "20251209",
    "Time": "224948",
    "bits": 16,
    "eps": 0.05,
    "alpha": 1.0,
    "beta": 1.0,
    "mask_reg": 0.1,
    "logit_reg": 0.01,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "noise_only_hf1",
    "run_name": "20251209-224948_bits16_eps0.05_alpha1.0_beta1.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251209-224948_bits16_eps0.05_alpha1.0_beta1.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1.png",
    "eval_exists": false,
    "metrics": {}
  },
  {
    "Date": "20251209",
    "Time": "153608",
    "bits": 16,
    "eps": 0.2,
    "alpha": 0.1,
    "beta": 0.1,
    "mask_reg": 0.01,
    "logit_reg": 0.01,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "full_hf0",
    "run_name": "20251209-153608_bits16_eps0.2_alpha0.1_beta0.1_mask0.01_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chfull_hf0",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251209-153608_bits16_eps0.2_alpha0.1_beta0.1_mask0.01_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chfull_hf0.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.2565,
        "snr": 16.4,
        "lsd": 0.009
      },
      "Noise (std=0.01)": {
        "ber": 0.4111,
        "snr": 16.4,
        "lsd": 0.009
      },
      "Resample (0.9x)": {
        "ber": 0.5018,
        "snr": 16.4,
        "lsd": 0.009
      },
      "Resample (1.1x)": {
        "ber": 0.5007,
        "snr": 16.4,
        "lsd": 0.009
      },
      "MP3 (128k)": {
        "ber": 0.3434,
        "snr": 16.4,
        "lsd": 0.009
      },
      "MP3 (64k)": {
        "ber": 0.3814,
        "snr": 16.4,
        "lsd": 0.009
      },
      "AAC (128k)": {
        "ber": 0.3441,
        "snr": 16.4,
        "lsd": 0.009
      },
      "Quant (12-bit)": {
        "ber": 0.3087,
        "snr": 16.4,
        "lsd": 0.009
      },
      "Random EQ": {
        "ber": 0.2892,
        "snr": 16.4,
        "lsd": 0.009
      }
    }
  },
  {
    "Date": "20251201",
    "Time": "164410",
    "bits": 16,
    "eps": 0.2,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0,
    "logit_reg": 0.0,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "noise_only",
    "run_name": "20251201-164410_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep20_chnoise_only",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251201-164410_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep20_chnoise_only.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.1682,
        "snr": 15.42,
        "lsd": 0.035
      },
      "Noise (std=0.01)": {
        "ber": 0.3302,
        "snr": 15.42,
        "lsd": 0.035
      },
      "Resample (0.9x)": {
        "ber": 0.391,
        "snr": 15.42,
        "lsd": 0.035
      },
      "Resample (1.1x)": {
        "ber": 0.4277,
        "snr": 15.42,
        "lsd": 0.035
      },
      "MP3 (128k)": {
        "ber": 0.2646,
        "snr": 15.42,
        "lsd": 0.035
      },
      "MP3 (64k)": {
        "ber": 0.3079,
        "snr": 15.42,
        "lsd": 0.035
      },
      "AAC (128k)": {
        "ber": 0.2417,
        "snr": 15.42,
        "lsd": 0.035
      },
      "Quant (12-bit)": {
        "ber": 0.23,
        "snr": 15.42,
        "lsd": 0.035
      },
      "Random EQ": {
        "ber": 0.316,
        "snr": 15.42,
        "lsd": 0.035
      }
    }
  },
  {
    "Date": "20251201",
    "Time": "125751",
    "bits": 16,
    "eps": 0.2,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0,
    "logit_reg": 0.0,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "noise_only",
    "run_name": "20251201-125751_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep10_chnoise_only",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251201-125751_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep10_chnoise_only.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.1915,
        "snr": 18.35,
        "lsd": 0.019
      },
      "Noise (std=0.01)": {
        "ber": 0.3688,
        "snr": 18.35,
        "lsd": 0.019
      },
      "Resample (0.9x)": {
        "ber": 0.4492,
        "snr": 18.35,
        "lsd": 0.019
      },
      "Resample (1.1x)": {
        "ber": 0.4593,
        "snr": 18.35,
        "lsd": 0.019
      },
      "MP3 (128k)": {
        "ber": 0.2709,
        "snr": 18.35,
        "lsd": 0.019
      },
      "MP3 (64k)": {
        "ber": 0.3254,
        "snr": 18.35,
        "lsd": 0.019
      },
      "AAC (128k)": {
        "ber": 0.2588,
        "snr": 18.35,
        "lsd": 0.019
      },
      "Quant (12-bit)": {
        "ber": 0.2569,
        "snr": 18.35,
        "lsd": 0.019
      },
      "Random EQ": {
        "ber": 0.2905,
        "snr": 18.35,
        "lsd": 0.019
      }
    }
  },
  {
    "Date": "20251127",
    "Time": "184226",
    "bits": 16,
    "eps": 0.1,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0,
    "logit_reg": 0.0,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 15,
    "channel": "none",
    "run_name": "20251127-184226_bits16_eps0.1_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep15_chnone",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251127-184226_bits16_eps0.1_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep15_chnone.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.273,
        "snr": 23.18,
        "lsd": 0.009
      },
      "Noise (std=0.01)": {
        "ber": 0.3869,
        "snr": 23.18,
        "lsd": 0.009
      },
      "Resample (0.9x)": {
        "ber": 0.4122,
        "snr": 23.18,
        "lsd": 0.009
      },
      "Resample (1.1x)": {
        "ber": 0.4633,
        "snr": 23.18,
        "lsd": 0.009
      },
      "MP3 (128k)": {
        "ber": 0.3653,
        "snr": 23.18,
        "lsd": 0.009
      },
      "MP3 (64k)": {
        "ber": 0.3773,
        "snr": 23.18,
        "lsd": 0.009
      },
      "AAC (128k)": {
        "ber": 0.31,
        "snr": 23.18,
        "lsd": 0.009
      },
      "Quant (12-bit)": {
        "ber": 0.3055,
        "snr": 23.18,
        "lsd": 0.009
      },
      "Random EQ": {
        "ber": 0.4071,
        "snr": 23.18,
        "lsd": 0.009
      }
    }
  },
  {
    "Date": "20251127",
    "Time": "142640",
    "bits": 16,
    "eps": 0.3,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0,
    "logit_reg": 0.0,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "none",
    "run_name": "20251127-142640_bits16_eps0.3_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep10_chnone",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251127-142640_bits16_eps0.3_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep10_chnone.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.116,
        "snr": 12.67,
        "lsd": 0.047
      },
      "Noise (std=0.01)": {
        "ber": 0.3352,
        "snr": 12.67,
        "lsd": 0.047
      },
      "Resample (0.9x)": {
        "ber": 0.4439,
        "snr": 12.67,
        "lsd": 0.047
      },
      "Resample (1.1x)": {
        "ber": 0.4573,
        "snr": 12.67,
        "lsd": 0.047
      },
      "MP3 (128k)": {
        "ber": 0.212,
        "snr": 12.67,
        "lsd": 0.047
      },
      "MP3 (64k)": {
        "ber": 0.2702,
        "snr": 12.67,
        "lsd": 0.047
      },
      "AAC (128k)": {
        "ber": 0.1912,
        "snr": 12.67,
        "lsd": 0.047
      },
      "Quant (12-bit)": {
        "ber": 0.186,
        "snr": 12.67,
        "lsd": 0.047
      },
      "Random EQ": {
        "ber": 0.223,
        "snr": 12.67,
        "lsd": 0.047
      }
    }
  },
  {
    "Date": "20251127",
    "Time": "120115",
    "bits": 16,
    "eps": 0.2,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0,
    "logit_reg": 0.0,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "none",
    "run_name": "20251127-120115_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep10_chnone",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251127-120115_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep10_chnone.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.1767,
        "snr": 16.55,
        "lsd": 0.022
      },
      "Noise (std=0.01)": {
        "ber": 0.35,
        "snr": 16.55,
        "lsd": 0.022
      },
      "Resample (0.9x)": {
        "ber": 0.4196,
        "snr": 16.55,
        "lsd": 0.022
      },
      "Resample (1.1x)": {
        "ber": 0.4511,
        "snr": 16.55,
        "lsd": 0.022
      },
      "MP3 (128k)": {
        "ber": 0.249,
        "snr": 16.55,
        "lsd": 0.022
      },
      "MP3 (64k)": {
        "ber": 0.3001,
        "snr": 16.55,
        "lsd": 0.022
      },
      "AAC (128k)": {
        "ber": 0.225,
        "snr": 16.55,
        "lsd": 0.022
      },
      "Quant (12-bit)": {
        "ber": 0.2324,
        "snr": 16.55,
        "lsd": 0.022
      },
      "Random EQ": {
        "ber": 0.3101,
        "snr": 16.55,
        "lsd": 0.022
      }
    }
  },
  {
    "Date": "20251127",
    "Time": "092954",
    "bits": 16,
    "eps": 0.1,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0,
    "logit_reg": 0.0,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "none",
    "run_name": "20251127-092954_bits16_eps0.1_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep10_chnone",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251127-092954_bits16_eps0.1_alpha0.0_beta0.0_mask0.0_logit0.0_decLR3e-4_decSteps0_bs32_ep10_chnone.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.3024,
        "snr": 30.61,
        "lsd": 0.007
      },
      "Noise (std=0.01)": {
        "ber": 0.4108,
        "snr": 30.61,
        "lsd": 0.007
      },
      "Resample (0.9x)": {
        "ber": 0.4377,
        "snr": 30.61,
        "lsd": 0.007
      },
      "Resample (1.1x)": {
        "ber": 0.4653,
        "snr": 30.61,
        "lsd": 0.007
      },
      "MP3 (128k)": {
        "ber": 0.3574,
        "snr": 30.61,
        "lsd": 0.007
      },
      "MP3 (64k)": {
        "ber": 0.3832,
        "snr": 30.61,
        "lsd": 0.007
      },
      "AAC (128k)": {
        "ber": 0.336,
        "snr": 30.61,
        "lsd": 0.007
      },
      "Quant (12-bit)": {
        "ber": 0.3389,
        "snr": 30.61,
        "lsd": 0.007
      },
      "Random EQ": {
        "ber": 0.4114,
        "snr": 30.61,
        "lsd": 0.007
      }
    }
  },
  {
    "Date": "20251126",
    "Time": "234814",
    "bits": 16,
    "eps": 0.2,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0,
    "logit_reg": 0.0,
    "decoder_lr": "5e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "none",
    "run_name": "20251126-234814_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR5e-4_decSteps0_bs32_ep10_chnone",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251126-234814_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR5e-4_decSteps0_bs32_ep10_chnone.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.2047,
        "snr": 15.81,
        "lsd": 0.031
      },
      "Noise (std=0.01)": {
        "ber": 0.4322,
        "snr": 15.81,
        "lsd": 0.031
      },
      "Resample (0.9x)": {
        "ber": 0.5003,
        "snr": 15.81,
        "lsd": 0.031
      },
      "Resample (1.1x)": {
        "ber": 0.5004,
        "snr": 15.81,
        "lsd": 0.031
      },
      "MP3 (128k)": {
        "ber": 0.2991,
        "snr": 15.81,
        "lsd": 0.031
      },
      "MP3 (64k)": {
        "ber": 0.3557,
        "snr": 15.81,
        "lsd": 0.031
      },
      "AAC (128k)": {
        "ber": 0.29,
        "snr": 15.81,
        "lsd": 0.031
      },
      "Quant (12-bit)": {
        "ber": 0.2871,
        "snr": 15.81,
        "lsd": 0.031
      },
      "Random EQ": {
        "ber": 0.2525,
        "snr": 15.81,
        "lsd": 0.031
      }
    }
  }
];