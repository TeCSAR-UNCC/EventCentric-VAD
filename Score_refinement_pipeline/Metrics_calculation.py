import pandas as pd
import numpy as np
from pathlib import Path


results_dir = Path("")

window_size = 24
apply_filter_short_events = True
min_duration = 6

# mAP Thresholds
tiou_thresholds = [0.2, 0.3, 0.4, 0.5]

def get_stgnf_intervals(array):
    
    padded = np.concatenate([[0], array, [0]])
    diff = np.diff(padded)
    starts = np.where(diff == 1)[0]
    ends = np.where(diff == -1)[0] - 1
    return list(zip(starts, ends))

def calculate_tiou(int_a, int_b):
    s1, e1 = int_a
    s2, e2 = int_b
    intersection = max(0, min(e1, e2) - max(s1, s2) + 1)
    union = (e1 - s1 + 1) + (e2 - s2 + 1) - intersection
    return intersection / union if union > 0 else 0

# Load All Data
all_gt = []
all_pred = []

for csv_file in sorted(results_dir.glob('*.csv')):
    df = pd.read_csv(csv_file, header=None)
    gt_ints = get_stgnf_intervals(df.iloc[:, 0].values)
    pred_ints = get_stgnf_intervals(df.iloc[:, 3].values)
    
    if apply_filter_short_events:
        pred_ints = [p for p in pred_ints if (p[1] - p[0] + 1) > min_duration]
        
    all_gt.append(gt_ints)
    all_pred.append(pred_ints)

# Calculate total dataset stats (constant across thresholds)
total_gt_count = sum(len(g) for g in all_gt)
total_pred_count = sum(len(p) for p in all_pred)

# Dataset Overview 
print("\n" + "="*50)
print(f"SHANGHAITECH DATASET TOTALS")
print("="*50)
print(f"Total Ground Truth (GT) Events: {total_gt_count}")
print(f"Total Predicted Events:        {total_pred_count}")
print(f"Event Count Error (Pred-GT):   {total_pred_count - total_gt_count}")
print("="*50 + "\n")

# Loop Through Thresholds 
precisions_per_threshold = []

print(f"Calculating full metrics at different tIoU thresholds...")
print(f"{'tIoU':<6} | {'TP':<5} | {'FP':<5} | {'FN':<5} | {'Prec':<8} | {'Rec':<8} | {'F1':<8}")
print("-" * 65)

for thresh in tiou_thresholds:
    total_tp = 0
    
    for gt_ints, pred_ints in zip(all_gt, all_pred):
        matched_indices = set()
        file_tp = 0
        
        for g_int in gt_ints:
            best_iou = 0
            best_p_idx = -1
            for p_idx, p_int in enumerate(pred_ints):
                if p_idx in matched_indices:
                    continue
                iou = calculate_tiou(g_int, p_int)
                if iou > best_iou:
                    best_iou = iou
                    best_p_idx = p_idx
            
            if best_iou >= thresh:
                file_tp += 1
                matched_indices.add(best_p_idx)
        
        total_tp += file_tp
        
    # Calculate Precision, Recall, and F1
    total_fp = total_pred_count - total_tp
    total_fn = total_gt_count - total_tp
    
    prec = total_tp / total_pred_count if total_pred_count > 0 else 0
    rec = total_tp / total_gt_count if total_gt_count > 0 else 0
    f1 = 2 * (prec * rec) / (prec + rec) if (prec + rec) > 0 else 0
    
    precisions_per_threshold.append(prec)
    print(f"{thresh:<6.1f} | {total_tp:<5} | {total_fp:<5} | {total_fn:<5} | {prec:<8.4f} | {rec:<8.4f} | {f1:<8.4f}")

# Final mean average precision Calculation
mAP = np.mean(precisions_per_threshold)

print("\n" + "="*50)
print(f"FINAL mAP RESULT: {mAP:.4f}")
print("="*50)


all_durations = [(p[1] - p[0] + 1) for file_preds in all_pred for p in file_preds]

if all_durations:
    shortest_event = min(all_durations)
    longest_event = max(all_durations)
    avg_event = np.mean(all_durations)
    
    print("\n" + "-"*30)
    print("PREDICTED EVENT STATISTICS")
    print("-"*30)
    print(f"Shortest Event: {shortest_event} frames")
    print(f"Longest Event:  {longest_event} frames")
    print(f"Average Event:  {avg_event:.2f} frames")
    print("-"*30)
else:
    print("\nNo events were predicted with the current threshold/min_duration.")