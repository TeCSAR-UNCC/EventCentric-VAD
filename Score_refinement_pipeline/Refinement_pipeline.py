import pandas as pd
import numpy as np
import os
from pathlib import Path
from scipy.ndimage import gaussian_filter1d

input_dir = Path("") 
output_dir = Path("")

threshold=0.48
window_size=24
stride = 6  
use_sliding = True
sigma = 7  

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    
def apply_gaussian_smoothing(scores, sigma_val=7):
    """
    Applies Gaussian smoothing iteratively matching the training logic.
    """
    s = scores.copy()
    for sig in range(1, sigma_val):
        s = gaussian_filter1d(s, sigma=sig)
    return s


def apply_flexible_smoothing(series, window=24, stride=6):
    arr = series.values.astype(int).copy()
    n = len(arr)
    output = np.zeros(n, dtype=int)
    offset = stride 

    # 1. Main Loop (Processes all full windows)
    for i in range(0, n - window + 1, stride):
        block = arr[i : i + window]
        winner = 1 if np.sum(block == 1) > np.sum(block == 0) else 0
        
        start_idx = i + offset
        end_idx = start_idx + stride
        output[start_idx : end_idx] = winner
        
    # 2. Tail Handling (Processes the leftover frames)
    # Find where the last block in the loop finished
    last_processed_end = ((n - window) // stride * stride) + offset + stride
    
    if last_processed_end < n:
        # Take whatever frames are left at the end
        remaining_block = arr[last_processed_end:]
        # Simple majority vote on the remaining frames
        winner = 1 if np.sum(remaining_block == 1) > np.sum(remaining_block == 0) else 0
        output[last_processed_end:] = winner
        
    return output


print(f"Starting Post-Processing...")
print(f"Threshold : {threshold} | Window: {window_size} | Stride: {stride}")

for csv_file in sorted(input_dir.glob("*.csv")):
    
    df = pd.read_csv(csv_file, header=None, names=['GT', 'Score'])
    
    # Gaussian Smoothing on Raw Scores
    df['Smoothed_Score'] = apply_gaussian_smoothing(df['Score'].values, sigma)
    
    # Binarization
    df['Binarized'] = np.where(df['Smoothed_Score'] > threshold, 1, 0)
    
    df['Smoothed_Binarized'] = apply_flexible_smoothing(df['Binarized'], window_size, stride)
    
    output_path = output_dir / csv_file.name
    df[['GT', 'Smoothed_Score', 'Binarized', 'Smoothed_Binarized']].to_csv(output_path, index=False, header=False)

print(f"Final processed files saved to: {output_dir}")