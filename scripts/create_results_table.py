#!/home/bmainbird/UL/sound-production/project/venv/bin/python
import os
import glob
import json
import re
import pandas as pd
import argparse

def parse_filename(filename):
    # 20251126-234814_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR5e-4_decSteps0_bs32_ep10_chnone.txt
    pattern = r"^(\d{8})-(\d{6})_bits(\d+)_eps([\d\.]+)_alpha([\d\.]+)_beta([\d\.]+)_mask([\d\.]+)_logit([\d\.]+)_decLR([\d\.e\-]+)_decSteps(\d+)_bs(\d+)_ep(\d+)_ch(\w+)\.txt$"
    match = re.match(pattern, filename)
    if match:
        return {
            "Date": match.group(1),
            "Time": match.group(2),
            "bits": int(match.group(3)),
            "eps": float(match.group(4)),
            "alpha": float(match.group(5)),
            "beta": float(match.group(6)),
            "mask_reg": float(match.group(7)),
            "logit_reg": float(match.group(8)),
            "decoder_lr": match.group(9), # Keep as string to preserve format like 5e-4
            "decoder_steps": int(match.group(10)),
            "batch-size": int(match.group(11)),
            "Epochs": int(match.group(12)),
            "channel": match.group(13)
        }
    return None

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(project_root, "results")
    plots_dir = os.path.join(project_root, "plots")
    checkpoints_dir = os.path.join(project_root, "checkpoints")

    txt_files = glob.glob(os.path.join(results_dir, "*.txt"))
    
    data = []

    for txt_path in txt_files:
        filename = os.path.basename(txt_path)
        run_name = os.path.splitext(filename)[0]
        
        parsed = parse_filename(filename)
        if not parsed:
            print(f"Skipping {filename} (does not match pattern)")
            continue

        row = parsed.copy()
        
        # Check checkpoints
        enc_ckpt = os.path.join(checkpoints_dir, f"{run_name}_encoder.pt")
        dec_ckpt = os.path.join(checkpoints_dir, f"{run_name}_decoder.pt")
        row["enc_checkpoint exists"] = os.path.exists(enc_ckpt)
        row["dec_checkpoint exists"] = os.path.exists(dec_ckpt)

        # Check plot
        plot_path = os.path.join(plots_dir, f"{run_name}.png")
        if os.path.exists(plot_path):
            row["Plot"] = plot_path
        else:
            row["Plot"] = ""

        # Check eval
        eval_dir = os.path.join(results_dir, f"eval_{run_name}")
        metrics_path = os.path.join(eval_dir, "metrics.json")
        
        row["Eval exists"] = False
        
        if os.path.exists(metrics_path):
            row["Eval exists"] = True
            try:
                with open(metrics_path, "r") as f:
                    metrics = json.load(f)
                
                for attack_name, scores in metrics.items():
                    # Clean attack name for column header
                    # e.g. "Noise (std=0.01)" -> "Noise" or keep as is?
                    # User requested "Eval: Identity BER", etc.
                    # I will keep the full name to distinguish different parameters if any
                    
                    prefix = f"Eval: {attack_name}"
                    
                    ber = scores.get("ber")
                    snr = scores.get("snr")
                    lsd = scores.get("lsd")

                    if ber is not None:
                        row[f"{prefix} BER"] = round(ber, 2)
                    if snr is not None:
                        row[f"{prefix} SNR"] = round(snr, 2)
                    if lsd is not None:
                        row[f"{prefix} LSD"] = round(lsd, 2)

            except Exception as e:
                print(f"Error reading metrics for {run_name}: {e}")

        data.append(row)

    df = pd.DataFrame(data)
    
    # Reorder columns to match user request approx
    base_cols = [
        "Date", "Time", "bits", "channel", "Epochs", "batch-size", "eps", 
        "decoder_lr", "decoder_steps", "alpha", "beta", 
        "mask_reg", "logit_reg", 
        "Plot", "enc_checkpoint exists", "dec_checkpoint exists", "Eval exists"
    ]
    
    # Find all Eval columns
    eval_cols = [c for c in df.columns if c.startswith("Eval: ")]
    # Sort eval columns to group by attack type then metric
    eval_cols.sort()

    # Combine
    final_cols = base_cols + eval_cols
    
    # Filter for columns that actually exist in df
    final_cols = [c for c in final_cols if c in df.columns]
    
    # Add any other columns found (like 'bits', 'channel' which weren't explicitly requested but parsed)
    other_cols = [c for c in df.columns if c not in final_cols]
    final_cols += other_cols

    df = df[final_cols]
    
    # Sort by Date and Time
    df = df.sort_values(by=["Date", "Time"], ascending=[False, False])

    output_csv = os.path.join(project_root, "results_table.csv")
    df.to_csv(output_csv, index=False)
    print(f"Saved results table to {output_csv}")

    # Try saving as ODS or XLSX if possible
    # User asked for LibreOffice file (ODS)
    # try:
    #     output_ods = os.path.join(project_root, "results_table.ods")
    #     df.to_excel(output_ods, engine="odf", index=False)
    #     print(f"Saved results table to {output_ods}")
    # except ImportError:
    #     print("odfpy not installed, skipping ODS export.")
    # except Exception as e:
    #     print(f"Could not save ODS: {e}")

if __name__ == "__main__":
    main()

