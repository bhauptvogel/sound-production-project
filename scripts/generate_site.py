#!/usr/bin/env python3
import os
import glob
import json
import re
import shutil
import argparse
import pandas as pd

def parse_filename(filename):
    # 20251126-234814_bits16_eps0.2_alpha0.0_beta0.0_mask0.0_logit0.0_decLR5e-4_decSteps0_bs32_ep10_chnone.txt
    pattern = r"^(\d{8})-(\d{6})_bits(\d+)_eps([\d\.e\-]+)_alpha([\d\.e\-]+)_beta([\d\.e\-]+)_mask([\d\.e\-]+)_logit([\d\.e\-]+)_decLR([\d\.e\-]+)_decSteps(\d+)_bs(\d+)_ep(\d+)_ch(\w+)\.txt$"
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
            "decoder_lr": match.group(9),
            "decoder_steps": int(match.group(10)),
            "batch_size": int(match.group(11)),
            "Epochs": int(match.group(12)),
            "channel": match.group(13)
        }
    return None

def main():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(project_root, "results")
    plots_dir = os.path.join(project_root, "plots")
    site_dir = os.path.join(project_root, "results_site")
    site_plots_dir = os.path.join(site_dir, "plots")
    checkpoints_dir = os.path.join(project_root, "checkpoints")

    # Ensure site plots dir exists
    os.makedirs(site_plots_dir, exist_ok=True)

    txt_files = glob.glob(os.path.join(results_dir, "*.txt"))
    
    data = []

    print(f"Found {len(txt_files)} result files.")

    for txt_path in txt_files:
        filename = os.path.basename(txt_path)
        run_name = os.path.splitext(filename)[0]
        
        parsed = parse_filename(filename)
        if not parsed:
            print(f"Skipping {filename} (does not match pattern)")
            continue

        row = parsed.copy()
        row["run_name"] = run_name
        
        # Check checkpoints
        enc_ckpt = os.path.join(checkpoints_dir, f"{run_name}_encoder.pt")
        dec_ckpt = os.path.join(checkpoints_dir, f"{run_name}_decoder.pt")
        row["enc_checkpoint"] = os.path.exists(enc_ckpt)
        row["dec_checkpoint"] = os.path.exists(dec_ckpt)

        # Handle Plot
        plot_filename = f"{run_name}.png"
        src_plot_path = os.path.join(plots_dir, plot_filename)
        if os.path.exists(src_plot_path):
            dst_plot_path = os.path.join(site_plots_dir, plot_filename)
            shutil.copy2(src_plot_path, dst_plot_path)
            row["plot_url"] = f"plots/{plot_filename}"
        else:
            row["plot_url"] = None

        # Check eval metrics
        eval_dir = os.path.join(results_dir, f"eval_{run_name}")
        metrics_path = os.path.join(eval_dir, "metrics.json")
        
        row["eval_exists"] = False
        row["metrics"] = {}
        
        if os.path.exists(metrics_path):
            row["eval_exists"] = True
            try:
                with open(metrics_path, "r") as f:
                    metrics = json.load(f)
                
                # Flatten metrics for easier table display or keep structured
                # We'll keep structured for JS to handle, but maybe flatten simple ones
                for attack_name, scores in metrics.items():
                    # Store per attack
                    row["metrics"][attack_name] = {
                        "ber": round(scores.get("ber", -1), 4) if scores.get("ber") is not None else None,
                        "snr": round(scores.get("snr", -1), 2) if scores.get("snr") is not None else None,
                        "lsd": round(scores.get("lsd", -1), 3) if scores.get("lsd") is not None else None
                    }

            except Exception as e:
                print(f"Error reading metrics for {run_name}: {e}")

        data.append(row)

    # Sort by Date and Time (descending)
    data.sort(key=lambda x: (x["Date"], x["Time"]), reverse=True)

    output_js = os.path.join(site_dir, "data.js")
    with open(output_js, "w") as f:
        json_str = json.dumps(data, indent=2)
        f.write(f"window.resultsData = {json_str};")
    
    print(f"Generated site data at {output_js} with {len(data)} entries.")

    # CSV Generation
    csv_data = []
    
    # Collect all unique attack names first to ensure consistent columns
    all_attack_names = set()
    for row in data:
        if row.get("eval_exists") and row.get("metrics"):
            all_attack_names.update(row["metrics"].keys())
    
    sorted_attack_names = sorted(list(all_attack_names))

    for row in data:
        if not row.get("eval_exists"):
            continue
            
        csv_row = {
            "date": row["Date"],
            "time": row["Time"],
            "n-bits": row["bits"],
            "eps": row["eps"],
            "alpha": row["alpha"],
            "mask_reg": row["mask_reg"],
            "logit_reg": row["logit_reg"],
            "decoder_steps": row["decoder_steps"],
            "decoder_lr": row["decoder_lr"],
            "batch_size": row["batch_size"],
            "epochs": row["Epochs"],
            "channel": row["channel"],
            "plot_url": row["plot_url"] if row["plot_url"] else ""
        }
        
        # Add metrics
        if row.get("metrics"):
            for attack in sorted_attack_names:
                # Clean attack name for column header (lowercase, spaces to underscores)
                clean_attack = attack.lower().replace(" ", "_").replace("-", "_")
                
                scores = row["metrics"].get(attack, {})
                csv_row[f"eval_ber_{clean_attack}"] = scores.get("ber", "")
                csv_row[f"eval_snr_{clean_attack}"] = scores.get("snr", "")
                csv_row[f"eval_lsd_{clean_attack}"] = scores.get("lsd", "")
        
        csv_data.append(csv_row)

    if csv_data:
        df = pd.DataFrame(csv_data)
        output_csv = os.path.join(site_dir, "data.csv")
        df.to_csv(output_csv, index=False)
        print(f"Generated CSV data at {output_csv} with {len(csv_data)} entries.")
    else:
        print("No evaluation data found, skipping CSV generation.")

if __name__ == "__main__":
    main()

