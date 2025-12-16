window.resultsData = [
  {
    "Date": "20251216",
    "Time": "060940",
    "bits": 16,
    "eps": 0.4,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 2,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "full_hf1",
    "run_name": "20251216-060940_bits16_eps0.4_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps2_bs32_ep20_chfull_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251216-060940_bits16_eps0.4_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps2_bs32_ep20_chfull_hf1.png",
    "eval_exists": false,
    "metrics": {}
  },
  {
    "Date": "20251214",
    "Time": "040608",
    "bits": 16,
    "eps": 0.4,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 1,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "full_hf1",
    "run_name": "20251214-040608_bits16_eps0.4_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chfull_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251214-040608_bits16_eps0.4_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chfull_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.122,
        "snr": 10.38,
        "lsd": 0.053
      },
      "Noise (std=0.01)": {
        "ber": 0.3237,
        "snr": 8.35,
        "lsd": 12.553
      },
      "Resample (0.9x)": {
        "ber": 0.4512,
        "snr": -2.99,
        "lsd": 2.579
      },
      "Resample (1.1x)": {
        "ber": 0.4498,
        "snr": -2.84,
        "lsd": 14.217
      },
      "MP3 (128k)": {
        "ber": 0.1892,
        "snr": 10.37,
        "lsd": 2.118
      },
      "MP3 (64k)": {
        "ber": 0.2561,
        "snr": 9.64,
        "lsd": 5.497
      },
      "AAC (128k)": {
        "ber": 0.1785,
        "snr": 10.36,
        "lsd": 1.689
      },
      "Quant (12-bit)": {
        "ber": 0.1845,
        "snr": 10.3,
        "lsd": 1.322
      },
      "Random EQ": {
        "ber": 0.1519,
        "snr": 7.94,
        "lsd": 0.2
      }
    }
  },
  {
    "Date": "20251213",
    "Time": "223646",
    "bits": 16,
    "eps": 0.4,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 1,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "none_hf1",
    "run_name": "20251213-223646_bits16_eps0.4_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnone_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251213-223646_bits16_eps0.4_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnone_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.0751,
        "snr": 10.4,
        "lsd": 0.067
      },
      "Noise (std=0.01)": {
        "ber": 0.2889,
        "snr": 8.49,
        "lsd": 12.357
      },
      "Resample (0.9x)": {
        "ber": 0.4071,
        "snr": -1.88,
        "lsd": 2.592
      },
      "Resample (1.1x)": {
        "ber": 0.4346,
        "snr": -1.78,
        "lsd": 14.261
      },
      "MP3 (128k)": {
        "ber": 0.1477,
        "snr": 9.56,
        "lsd": 2.104
      },
      "MP3 (64k)": {
        "ber": 0.2158,
        "snr": 8.99,
        "lsd": 5.593
      },
      "AAC (128k)": {
        "ber": 0.1286,
        "snr": 10.17,
        "lsd": 1.578
      },
      "Quant (12-bit)": {
        "ber": 0.1299,
        "snr": 10.33,
        "lsd": 1.357
      },
      "Random EQ": {
        "ber": 0.222,
        "snr": 8.96,
        "lsd": 0.217
      }
    }
  },
  {
    "Date": "20251213",
    "Time": "164734",
    "bits": 16,
    "eps": 0.4,
    "alpha": 0.1,
    "beta": 0.1,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 1,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "full_hf1",
    "run_name": "20251213-164734_bits16_eps0.4_alpha0.1_beta0.1_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chfull_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251213-164734_bits16_eps0.4_alpha0.1_beta0.1_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chfull_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.1231,
        "snr": 11.58,
        "lsd": 0.034
      },
      "Noise (std=0.01)": {
        "ber": 0.3363,
        "snr": 9.5,
        "lsd": 12.388
      },
      "Resample (0.9x)": {
        "ber": 0.4812,
        "snr": -1.94,
        "lsd": 2.485
      },
      "Resample (1.1x)": {
        "ber": 0.4743,
        "snr": -1.83,
        "lsd": 14.2
      },
      "MP3 (128k)": {
        "ber": 0.2131,
        "snr": 10.46,
        "lsd": 1.979
      },
      "MP3 (64k)": {
        "ber": 0.283,
        "snr": 9.76,
        "lsd": 5.414
      },
      "AAC (128k)": {
        "ber": 0.2011,
        "snr": 11.26,
        "lsd": 1.512
      },
      "Quant (12-bit)": {
        "ber": 0.1934,
        "snr": 11.52,
        "lsd": 1.258
      },
      "Random EQ": {
        "ber": 0.1608,
        "snr": 9.24,
        "lsd": 0.181
      }
    }
  },
  {
    "Date": "20251213",
    "Time": "111111",
    "bits": 16,
    "eps": 0.4,
    "alpha": 0.1,
    "beta": 0.1,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 1,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "noise_only_hf1",
    "run_name": "20251213-111111_bits16_eps0.4_alpha0.1_beta0.1_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251213-111111_bits16_eps0.4_alpha0.1_beta0.1_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.0864,
        "snr": 10.12,
        "lsd": 0.047
      },
      "Noise (std=0.01)": {
        "ber": 0.2973,
        "snr": 8.1,
        "lsd": 12.631
      },
      "Resample (0.9x)": {
        "ber": 0.4236,
        "snr": -1.7,
        "lsd": 2.541
      },
      "Resample (1.1x)": {
        "ber": 0.4451,
        "snr": -1.59,
        "lsd": 14.181
      },
      "MP3 (128k)": {
        "ber": 0.1762,
        "snr": 9.18,
        "lsd": 2.075
      },
      "MP3 (64k)": {
        "ber": 0.2564,
        "snr": 8.69,
        "lsd": 5.551
      },
      "AAC (128k)": {
        "ber": 0.1542,
        "snr": 9.87,
        "lsd": 1.606
      },
      "Quant (12-bit)": {
        "ber": 0.1591,
        "snr": 10.05,
        "lsd": 1.319
      },
      "Random EQ": {
        "ber": 0.2093,
        "snr": 10.0,
        "lsd": 0.195
      }
    }
  },
  {
    "Date": "20251212",
    "Time": "182237",
    "bits": 16,
    "eps": 0.3,
    "alpha": 0.2,
    "beta": 0.2,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 2,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "noise_only_hf1",
    "run_name": "20251212-182237_bits16_eps0.3_alpha0.2_beta0.2_mask1e-4_logit1e-4_decLR1e-4_decSteps2_bs32_ep20_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251212-182237_bits16_eps0.3_alpha0.2_beta0.2_mask1e-4_logit1e-4_decLR1e-4_decSteps2_bs32_ep20_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.1462,
        "snr": 16.99,
        "lsd": 0.022
      },
      "Noise (std=0.01)": {
        "ber": 0.3119,
        "snr": 13.74,
        "lsd": 12.286
      },
      "Resample (0.9x)": {
        "ber": 0.4133,
        "snr": -2.54,
        "lsd": 2.522
      },
      "Resample (1.1x)": {
        "ber": 0.4296,
        "snr": -2.41,
        "lsd": 14.227
      },
      "MP3 (128k)": {
        "ber": 0.2277,
        "snr": 15.51,
        "lsd": 1.947
      },
      "MP3 (64k)": {
        "ber": 0.2926,
        "snr": 13.98,
        "lsd": 5.337
      },
      "AAC (128k)": {
        "ber": 0.2083,
        "snr": 16.45,
        "lsd": 1.468
      },
      "Quant (12-bit)": {
        "ber": 0.2004,
        "snr": 16.88,
        "lsd": 1.241
      },
      "Random EQ": {
        "ber": 0.2802,
        "snr": 9.95,
        "lsd": 0.168
      }
    }
  },
  {
    "Date": "20251212",
    "Time": "095901",
    "bits": 16,
    "eps": 0.3,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 1,
    "batch_size": 32,
    "Epochs": 30,
    "channel": "noise_only_hf1",
    "run_name": "20251212-095901_bits16_eps0.3_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep30_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251212-095901_bits16_eps0.3_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep30_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.1198,
        "snr": 12.5,
        "lsd": 0.049
      },
      "Noise (std=0.01)": {
        "ber": 0.3124,
        "snr": 10.07,
        "lsd": 12.629
      },
      "Resample (0.9x)": {
        "ber": 0.4257,
        "snr": -1.97,
        "lsd": 2.565
      },
      "Resample (1.1x)": {
        "ber": 0.443,
        "snr": -1.86,
        "lsd": 14.215
      },
      "MP3 (128k)": {
        "ber": 0.2022,
        "snr": 11.17,
        "lsd": 2.078
      },
      "MP3 (64k)": {
        "ber": 0.2711,
        "snr": 10.45,
        "lsd": 5.567
      },
      "AAC (128k)": {
        "ber": 0.1866,
        "snr": 12.14,
        "lsd": 1.605
      },
      "Quant (12-bit)": {
        "ber": 0.1861,
        "snr": 12.43,
        "lsd": 1.241
      },
      "Random EQ": {
        "ber": 0.2474,
        "snr": 10.41,
        "lsd": 0.195
      }
    }
  },
  {
    "Date": "20251212",
    "Time": "042158",
    "bits": 16,
    "eps": 0.3,
    "alpha": 0.2,
    "beta": 0.2,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 1,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "noise_only_hf1",
    "run_name": "20251212-042158_bits16_eps0.3_alpha0.2_beta0.2_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251212-042158_bits16_eps0.3_alpha0.2_beta0.2_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.1585,
        "snr": 20.56,
        "lsd": 0.017
      },
      "Noise (std=0.01)": {
        "ber": 0.3414,
        "snr": 16.28,
        "lsd": 12.532
      },
      "Resample (0.9x)": {
        "ber": 0.4455,
        "snr": -2.79,
        "lsd": 2.55
      },
      "Resample (1.1x)": {
        "ber": 0.4608,
        "snr": -2.64,
        "lsd": 14.213
      },
      "MP3 (128k)": {
        "ber": 0.2426,
        "snr": 19.1,
        "lsd": 1.977
      },
      "MP3 (64k)": {
        "ber": 0.2967,
        "snr": 16.86,
        "lsd": 5.382
      },
      "AAC (128k)": {
        "ber": 0.2336,
        "snr": 19.8,
        "lsd": 1.532
      },
      "Quant (12-bit)": {
        "ber": 0.221,
        "snr": 20.44,
        "lsd": 1.261
      },
      "Random EQ": {
        "ber": 0.2454,
        "snr": 9.95,
        "lsd": 0.166
      }
    }
  },
  {
    "Date": "20251211",
    "Time": "224523",
    "bits": 16,
    "eps": 0.4,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 1,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "noise_only_hf1",
    "run_name": "20251211-224523_bits16_eps0.4_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251211-224523_bits16_eps0.4_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.0943,
        "snr": 10.45,
        "lsd": 0.056
      },
      "Noise (std=0.01)": {
        "ber": 0.2925,
        "snr": 8.51,
        "lsd": 12.397
      },
      "Resample (0.9x)": {
        "ber": 0.4241,
        "snr": -1.78,
        "lsd": 2.57
      },
      "Resample (1.1x)": {
        "ber": 0.4367,
        "snr": -1.68,
        "lsd": 14.246
      },
      "MP3 (128k)": {
        "ber": 0.1813,
        "snr": 9.5,
        "lsd": 2.063
      },
      "MP3 (64k)": {
        "ber": 0.2551,
        "snr": 8.95,
        "lsd": 5.557
      },
      "AAC (128k)": {
        "ber": 0.1575,
        "snr": 10.2,
        "lsd": 1.569
      },
      "Quant (12-bit)": {
        "ber": 0.1611,
        "snr": 10.39,
        "lsd": 1.289
      },
      "Random EQ": {
        "ber": 0.2115,
        "snr": 9.73,
        "lsd": 0.202
      }
    }
  },
  {
    "Date": "20251211",
    "Time": "154331",
    "bits": 16,
    "eps": 0.3,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.0001,
    "logit_reg": 0.0001,
    "decoder_lr": "1e-4",
    "decoder_steps": 1,
    "batch_size": 32,
    "Epochs": 20,
    "channel": "noise_only_hf1",
    "run_name": "20251211-154331_bits16_eps0.3_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251211-154331_bits16_eps0.3_alpha0.0_beta0.0_mask1e-4_logit1e-4_decLR1e-4_decSteps1_bs32_ep20_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.122,
        "snr": 13.3,
        "lsd": 0.03
      },
      "Noise (std=0.01)": {
        "ber": 0.3193,
        "snr": 10.78,
        "lsd": 12.427
      },
      "Resample (0.9x)": {
        "ber": 0.4301,
        "snr": -2.11,
        "lsd": 2.554
      },
      "Resample (1.1x)": {
        "ber": 0.4508,
        "snr": -2.0,
        "lsd": 14.215
      },
      "MP3 (128k)": {
        "ber": 0.2135,
        "snr": 12.01,
        "lsd": 1.98
      },
      "MP3 (64k)": {
        "ber": 0.2793,
        "snr": 11.1,
        "lsd": 5.416
      },
      "AAC (128k)": {
        "ber": 0.1869,
        "snr": 12.94,
        "lsd": 1.523
      },
      "Quant (12-bit)": {
        "ber": 0.1866,
        "snr": 13.22,
        "lsd": 1.282
      },
      "Random EQ": {
        "ber": 0.2473,
        "snr": 10.26,
        "lsd": 0.178
      }
    }
  },
  {
    "Date": "20251211",
    "Time": "124606",
    "bits": 16,
    "eps": 0.5,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.1,
    "logit_reg": 0.01,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "noise_only_hf1",
    "run_name": "20251211-124606_bits16_eps0.5_alpha0.0_beta0.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251211-124606_bits16_eps0.5_alpha0.0_beta0.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.078,
        "snr": 13.68,
        "lsd": 0.031
      },
      "Noise (std=0.01)": {
        "ber": 0.2727,
        "snr": 11.29,
        "lsd": 12.609
      },
      "Resample (0.9x)": {
        "ber": 0.4502,
        "snr": -2.14,
        "lsd": 2.479
      },
      "Resample (1.1x)": {
        "ber": 0.4566,
        "snr": -2.02,
        "lsd": 14.179
      },
      "MP3 (128k)": {
        "ber": 0.1564,
        "snr": 12.15,
        "lsd": 1.92
      },
      "MP3 (64k)": {
        "ber": 0.2321,
        "snr": 11.32,
        "lsd": 5.344
      },
      "AAC (128k)": {
        "ber": 0.141,
        "snr": 13.23,
        "lsd": 1.553
      },
      "Quant (12-bit)": {
        "ber": 0.1375,
        "snr": 13.59,
        "lsd": 1.252
      },
      "Random EQ": {
        "ber": 0.1618,
        "snr": 9.79,
        "lsd": 0.179
      }
    }
  },
  {
    "Date": "20251211",
    "Time": "102617",
    "bits": 16,
    "eps": 0.5,
    "alpha": 0.1,
    "beta": 0.1,
    "mask_reg": 0.1,
    "logit_reg": 0.01,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "noise_only_hf1",
    "run_name": "20251211-102617_bits16_eps0.5_alpha0.1_beta0.1_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251211-102617_bits16_eps0.5_alpha0.1_beta0.1_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.0913,
        "snr": 15.69,
        "lsd": 0.03
      },
      "Noise (std=0.01)": {
        "ber": 0.2937,
        "snr": 12.67,
        "lsd": 12.512
      },
      "Resample (0.9x)": {
        "ber": 0.4829,
        "snr": -2.36,
        "lsd": 2.495
      },
      "Resample (1.1x)": {
        "ber": 0.4862,
        "snr": -2.22,
        "lsd": 14.177
      },
      "MP3 (128k)": {
        "ber": 0.1739,
        "snr": 13.89,
        "lsd": 1.933
      },
      "MP3 (64k)": {
        "ber": 0.2499,
        "snr": 12.78,
        "lsd": 5.35
      },
      "AAC (128k)": {
        "ber": 0.1673,
        "snr": 15.09,
        "lsd": 1.524
      },
      "Quant (12-bit)": {
        "ber": 0.1545,
        "snr": 15.57,
        "lsd": 1.251
      },
      "Random EQ": {
        "ber": 0.1316,
        "snr": 9.73,
        "lsd": 0.177
      }
    }
  },
  {
    "Date": "20251210",
    "Time": "233808",
    "bits": 16,
    "eps": 0.4,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.1,
    "logit_reg": 0.01,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "noise_only_hf1",
    "run_name": "20251210-233808_bits16_eps0.4_alpha0.0_beta0.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251210-233808_bits16_eps0.4_alpha0.0_beta0.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.1012,
        "snr": 19.23,
        "lsd": 0.02
      },
      "Noise (std=0.01)": {
        "ber": 0.2994,
        "snr": 15.27,
        "lsd": 12.475
      },
      "Resample (0.9x)": {
        "ber": 0.4482,
        "snr": -2.56,
        "lsd": 2.516
      },
      "Resample (1.1x)": {
        "ber": 0.4523,
        "snr": -2.43,
        "lsd": 14.259
      },
      "MP3 (128k)": {
        "ber": 0.1854,
        "snr": 16.64,
        "lsd": 1.889
      },
      "MP3 (64k)": {
        "ber": 0.2593,
        "snr": 14.91,
        "lsd": 5.291
      },
      "AAC (128k)": {
        "ber": 0.1785,
        "snr": 18.28,
        "lsd": 1.499
      },
      "Quant (12-bit)": {
        "ber": 0.1639,
        "snr": 19.11,
        "lsd": 1.246
      },
      "Random EQ": {
        "ber": 0.1977,
        "snr": 10.13,
        "lsd": 0.167
      }
    }
  },
  {
    "Date": "20251210",
    "Time": "211954",
    "bits": 16,
    "eps": 0.3,
    "alpha": 0.0,
    "beta": 0.0,
    "mask_reg": 0.1,
    "logit_reg": 0.01,
    "decoder_lr": "3e-4",
    "decoder_steps": 0,
    "batch_size": 32,
    "Epochs": 10,
    "channel": "noise_only_hf1",
    "run_name": "20251210-211954_bits16_eps0.3_alpha0.0_beta0.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1",
    "enc_checkpoint": true,
    "dec_checkpoint": true,
    "plot_url": "plots/20251210-211954_bits16_eps0.3_alpha0.0_beta0.0_mask0.1_logit0.01_decLR3e-4_decSteps0_bs32_ep10_chnoise_only_hf1.png",
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.1609,
        "snr": 20.93,
        "lsd": 0.013
      },
      "Noise (std=0.01)": {
        "ber": 0.3442,
        "snr": 16.28,
        "lsd": 12.546
      },
      "Resample (0.9x)": {
        "ber": 0.4754,
        "snr": -2.6,
        "lsd": 2.512
      },
      "Resample (1.1x)": {
        "ber": 0.4783,
        "snr": -2.47,
        "lsd": 14.251
      },
      "MP3 (128k)": {
        "ber": 0.239,
        "snr": 17.67,
        "lsd": 1.887
      },
      "MP3 (64k)": {
        "ber": 0.3069,
        "snr": 15.7,
        "lsd": 5.268
      },
      "AAC (128k)": {
        "ber": 0.2304,
        "snr": 19.69,
        "lsd": 1.511
      },
      "Quant (12-bit)": {
        "ber": 0.2195,
        "snr": 20.74,
        "lsd": 1.225
      },
      "Random EQ": {
        "ber": 0.2094,
        "snr": 10.2,
        "lsd": 0.16
      }
    }
  },
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
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.2035,
        "snr": 29.52,
        "lsd": 0.006
      },
      "Noise (std=0.01)": {
        "ber": 0.3795,
        "snr": 19.5,
        "lsd": 12.342
      },
      "Resample (0.9x)": {
        "ber": 0.4745,
        "snr": -2.82,
        "lsd": 2.526
      },
      "Resample (1.1x)": {
        "ber": 0.475,
        "snr": -2.68,
        "lsd": 14.299
      },
      "MP3 (128k)": {
        "ber": 0.2938,
        "snr": 22.39,
        "lsd": 1.839
      },
      "MP3 (64k)": {
        "ber": 0.3486,
        "snr": 18.85,
        "lsd": 5.189
      },
      "AAC (128k)": {
        "ber": 0.2775,
        "snr": 26.04,
        "lsd": 1.437
      },
      "Quant (12-bit)": {
        "ber": 0.2681,
        "snr": 29.26,
        "lsd": 1.247
      },
      "Random EQ": {
        "ber": 0.2862,
        "snr": 10.62,
        "lsd": 0.155
      }
    }
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
    "eval_exists": true,
    "metrics": {
      "Identity": {
        "ber": 0.4771,
        "snr": 53.33,
        "lsd": 0.001
      },
      "Noise (std=0.01)": {
        "ber": 0.4912,
        "snr": 20.53,
        "lsd": 12.547
      },
      "Resample (0.9x)": {
        "ber": 0.4986,
        "snr": -2.86,
        "lsd": 2.514
      },
      "Resample (1.1x)": {
        "ber": 0.5008,
        "snr": -2.71,
        "lsd": 14.256
      },
      "MP3 (128k)": {
        "ber": 0.4782,
        "snr": 24.49,
        "lsd": 1.682
      },
      "MP3 (64k)": {
        "ber": 0.4856,
        "snr": 20.01,
        "lsd": 4.981
      },
      "AAC (128k)": {
        "ber": 0.4777,
        "snr": 32.28,
        "lsd": 1.151
      },
      "Quant (12-bit)": {
        "ber": 0.4813,
        "snr": 50.28,
        "lsd": 1.282
      },
      "Random EQ": {
        "ber": 0.4818,
        "snr": 11.04,
        "lsd": 0.147
      }
    }
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
        "ber": 0.2545,
        "snr": 16.37,
        "lsd": 0.009
      },
      "Noise (std=0.01)": {
        "ber": 0.4094,
        "snr": 12.91,
        "lsd": 12.429
      },
      "Resample (0.9x)": {
        "ber": 0.5041,
        "snr": -2.24,
        "lsd": 2.494
      },
      "Resample (1.1x)": {
        "ber": 0.5067,
        "snr": -2.12,
        "lsd": 14.202
      },
      "MP3 (128k)": {
        "ber": 0.3424,
        "snr": 13.97,
        "lsd": 1.855
      },
      "MP3 (64k)": {
        "ber": 0.3774,
        "snr": 12.79,
        "lsd": 5.224
      },
      "AAC (128k)": {
        "ber": 0.3438,
        "snr": 15.63,
        "lsd": 1.443
      },
      "Quant (12-bit)": {
        "ber": 0.308,
        "snr": 16.19,
        "lsd": 1.287
      },
      "Random EQ": {
        "ber": 0.2872,
        "snr": 11.01,
        "lsd": 0.156
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
        "ber": 0.1673,
        "snr": 15.48,
        "lsd": 0.035
      },
      "Noise (std=0.01)": {
        "ber": 0.3296,
        "snr": 12.69,
        "lsd": 12.366
      },
      "Resample (0.9x)": {
        "ber": 0.3902,
        "snr": -2.24,
        "lsd": 2.584
      },
      "Resample (1.1x)": {
        "ber": 0.4276,
        "snr": -2.12,
        "lsd": 14.249
      },
      "MP3 (128k)": {
        "ber": 0.2653,
        "snr": 13.59,
        "lsd": 1.95
      },
      "MP3 (64k)": {
        "ber": 0.3139,
        "snr": 12.5,
        "lsd": 5.349
      },
      "AAC (128k)": {
        "ber": 0.2421,
        "snr": 15.0,
        "lsd": 1.458
      },
      "Quant (12-bit)": {
        "ber": 0.2296,
        "snr": 15.4,
        "lsd": 1.321
      },
      "Random EQ": {
        "ber": 0.3163,
        "snr": 10.75,
        "lsd": 0.182
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
        "ber": 0.194,
        "snr": 18.35,
        "lsd": 0.019
      },
      "Noise (std=0.01)": {
        "ber": 0.3665,
        "snr": 14.58,
        "lsd": 12.583
      },
      "Resample (0.9x)": {
        "ber": 0.4507,
        "snr": -2.42,
        "lsd": 2.544
      },
      "Resample (1.1x)": {
        "ber": 0.4532,
        "snr": -2.29,
        "lsd": 14.225
      },
      "MP3 (128k)": {
        "ber": 0.2739,
        "snr": 15.58,
        "lsd": 1.985
      },
      "MP3 (64k)": {
        "ber": 0.3207,
        "snr": 14.1,
        "lsd": 5.413
      },
      "AAC (128k)": {
        "ber": 0.2608,
        "snr": 17.48,
        "lsd": 1.526
      },
      "Quant (12-bit)": {
        "ber": 0.2586,
        "snr": 18.28,
        "lsd": 1.237
      },
      "Random EQ": {
        "ber": 0.2916,
        "snr": 10.67,
        "lsd": 0.166
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
        "ber": 0.2708,
        "snr": 23.2,
        "lsd": 0.009
      },
      "Noise (std=0.01)": {
        "ber": 0.3916,
        "snr": 17.01,
        "lsd": 12.565
      },
      "Resample (0.9x)": {
        "ber": 0.4161,
        "snr": -2.59,
        "lsd": 2.547
      },
      "Resample (1.1x)": {
        "ber": 0.4602,
        "snr": -2.45,
        "lsd": 14.249
      },
      "MP3 (128k)": {
        "ber": 0.3663,
        "snr": 18.44,
        "lsd": 1.873
      },
      "MP3 (64k)": {
        "ber": 0.376,
        "snr": 16.25,
        "lsd": 5.217
      },
      "AAC (128k)": {
        "ber": 0.3071,
        "snr": 21.45,
        "lsd": 1.24
      },
      "Quant (12-bit)": {
        "ber": 0.3043,
        "snr": 23.03,
        "lsd": 1.27
      },
      "Random EQ": {
        "ber": 0.4066,
        "snr": 10.75,
        "lsd": 0.157
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
        "ber": 0.1105,
        "snr": 12.69,
        "lsd": 0.047
      },
      "Noise (std=0.01)": {
        "ber": 0.3338,
        "snr": 10.34,
        "lsd": 12.61
      },
      "Resample (0.9x)": {
        "ber": 0.4436,
        "snr": -1.99,
        "lsd": 2.563
      },
      "Resample (1.1x)": {
        "ber": 0.4562,
        "snr": -1.88,
        "lsd": 14.224
      },
      "MP3 (128k)": {
        "ber": 0.2066,
        "snr": 11.32,
        "lsd": 2.072
      },
      "MP3 (64k)": {
        "ber": 0.2712,
        "snr": 10.59,
        "lsd": 5.557
      },
      "AAC (128k)": {
        "ber": 0.1883,
        "snr": 12.33,
        "lsd": 1.592
      },
      "Quant (12-bit)": {
        "ber": 0.1814,
        "snr": 12.64,
        "lsd": 1.283
      },
      "Random EQ": {
        "ber": 0.2161,
        "snr": 10.56,
        "lsd": 0.194
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
        "ber": 0.1789,
        "snr": 16.55,
        "lsd": 0.022
      },
      "Noise (std=0.01)": {
        "ber": 0.3499,
        "snr": 13.14,
        "lsd": 12.492
      },
      "Resample (0.9x)": {
        "ber": 0.4254,
        "snr": -2.31,
        "lsd": 2.562
      },
      "Resample (1.1x)": {
        "ber": 0.4534,
        "snr": -2.2,
        "lsd": 14.263
      },
      "MP3 (128k)": {
        "ber": 0.2467,
        "snr": 14.47,
        "lsd": 1.977
      },
      "MP3 (64k)": {
        "ber": 0.3004,
        "snr": 13.22,
        "lsd": 5.387
      },
      "AAC (128k)": {
        "ber": 0.2246,
        "snr": 15.9,
        "lsd": 1.509
      },
      "Quant (12-bit)": {
        "ber": 0.2346,
        "snr": 16.44,
        "lsd": 1.355
      },
      "Random EQ": {
        "ber": 0.3122,
        "snr": 10.53,
        "lsd": 0.17
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
        "ber": 0.2999,
        "snr": 30.63,
        "lsd": 0.007
      },
      "Noise (std=0.01)": {
        "ber": 0.4061,
        "snr": 19.85,
        "lsd": 12.277
      },
      "Resample (0.9x)": {
        "ber": 0.437,
        "snr": -2.77,
        "lsd": 2.527
      },
      "Resample (1.1x)": {
        "ber": 0.4633,
        "snr": -2.63,
        "lsd": 14.26
      },
      "MP3 (128k)": {
        "ber": 0.3587,
        "snr": 21.84,
        "lsd": 1.823
      },
      "MP3 (64k)": {
        "ber": 0.3819,
        "snr": 18.58,
        "lsd": 5.16
      },
      "AAC (128k)": {
        "ber": 0.3356,
        "snr": 26.86,
        "lsd": 1.243
      },
      "Quant (12-bit)": {
        "ber": 0.3311,
        "snr": 30.41,
        "lsd": 1.292
      },
      "Random EQ": {
        "ber": 0.4079,
        "snr": 10.84,
        "lsd": 0.155
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
        "ber": 0.2072,
        "snr": 15.81,
        "lsd": 0.031
      },
      "Noise (std=0.01)": {
        "ber": 0.4336,
        "snr": 12.77,
        "lsd": 12.568
      },
      "Resample (0.9x)": {
        "ber": 0.497,
        "snr": -2.2,
        "lsd": 2.537
      },
      "Resample (1.1x)": {
        "ber": 0.5017,
        "snr": -2.09,
        "lsd": 14.195
      },
      "MP3 (128k)": {
        "ber": 0.3009,
        "snr": 13.63,
        "lsd": 1.993
      },
      "MP3 (64k)": {
        "ber": 0.3591,
        "snr": 12.69,
        "lsd": 5.424
      },
      "AAC (128k)": {
        "ber": 0.2939,
        "snr": 15.25,
        "lsd": 1.549
      },
      "Quant (12-bit)": {
        "ber": 0.2874,
        "snr": 15.73,
        "lsd": 1.363
      },
      "Random EQ": {
        "ber": 0.2545,
        "snr": 10.89,
        "lsd": 0.178
      }
    }
  }
];