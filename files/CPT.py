import pandas as pd
import numpy as np
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
CSV_INPUT = "robot_sensor_data_labeled.csv"
CPT_OUTPUT_DIR = "CPTs"
DISCRETIZED_CSV = "robot_sensor_data_discretized.csv"
os.makedirs(CPT_OUTPUT_DIR, exist_ok=True)

# Sensor columns
IR_SENSORS = [f"IR{i+1}" for i in range(7)]
IR_BIN_LABELS = ["Near", "Medium", "Far"]

# Label column
LABEL_COLUMN = "Location"

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv(CSV_INPUT)
print("✅ CSV loaded. Total rows:", len(df))

# ----------------------------
# CLEAN LABELS
# ----------------------------
df[LABEL_COLUMN] = df[LABEL_COLUMN].astype(str).str.strip()
print("✅ Unique labels:", df[LABEL_COLUMN].unique())

# ----------------------------
# STEP 1: AUTOMATICALLY DEFINE IR BINS
# ----------------------------
ir_bins_dict = {}
for ir in IR_SENSORS:
    min_val = df[ir].min()
    max_val = df[ir].max()
    # define 3 bins spanning the range
    bins = [min_val - 1, min_val + (max_val-min_val)/3, min_val + 2*(max_val-min_val)/3, max_val + 1]
    ir_bins_dict[ir] = bins
    print(f"IR sensor {ir}: bins = {bins}")

# ----------------------------
# STEP 2: DISCRETIZE IR SENSORS
# ----------------------------
for ir in IR_SENSORS:
    bins = ir_bins_dict[ir]
    df[f"{ir}_bin"] = pd.cut(df[ir], bins=bins, labels=IR_BIN_LABELS, include_lowest=True)

# Quick check
print(df[[*IR_SENSORS, *[f"{ir}_bin" for ir in IR_SENSORS]]].head(5))

# ----------------------------
# STEP 3: COMPUTE CPTs
# ----------------------------
for ir in IR_SENSORS:
    bin_col = f"{ir}_bin"
    # Count occurrences
    cpt_counts = df.groupby([LABEL_COLUMN, bin_col]).size().unstack(fill_value=0)
    # Normalize per row to get probabilities
    cpt = cpt_counts.div(cpt_counts.sum(axis=1), axis=0)
    # Save CPT to CSV
    cpt_file = os.path.join(CPT_OUTPUT_DIR, f"CPT_{ir}_vs_{LABEL_COLUMN}.csv")
    cpt.to_csv(cpt_file)
    print(f"✅ CPT saved: {cpt_file}")
    print(cpt.head(), "\n")

# ----------------------------
# SAVE DISCRETIZED CSV
# ----------------------------
df.to_csv(DISCRETIZED_CSV, index=False)
print("✅ Discretized CSV saved as:", DISCRETIZED_CSV)
print("✅ All CPTs computed and saved in folder:", CPT_OUTPUT_DIR)
