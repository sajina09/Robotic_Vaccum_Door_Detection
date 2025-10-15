import pandas as pd
import numpy as np
import os

# ----------------------------
# CONFIGURATION
# ----------------------------
CSV_INPUT = "robot_sensor_data.csv"       # Raw data collected from the robot
CPT_OUTPUT_DIR = "CPTs"                   # Folder to save CPTs
DISCRETIZED_CSV = "robot_sensor_data_discretized.csv"

os.makedirs(CPT_OUTPUT_DIR, exist_ok=True)

# Only IR7 is used for Bayesian Network
IR_SENSOR = "IR7"
IR_BIN_LABELS = ["Near", "Medium", "Far"]
LABEL_COLUMN = "label"

# ----------------------------
# LOAD DATA
# ----------------------------
df = pd.read_csv(CSV_INPUT)
print("CSV loaded. Total rows:", len(df))
df[LABEL_COLUMN] = df[LABEL_COLUMN].astype(str).str.strip()
print("Unique labels:", df[LABEL_COLUMN].unique())

# ----------------------------
# STEP 1: DISCRETIZE IR7
# ----------------------------
min_val, max_val = df[IR_SENSOR].min(), df[IR_SENSOR].max()
bins = [min_val - 0.01,
        min_val + (max_val - min_val)/3,
        min_val + 2*(max_val - min_val)/3,
        max_val + 0.01]
df[f"{IR_SENSOR}_bin"] = pd.cut(df[IR_SENSOR], bins=bins, labels=IR_BIN_LABELS, include_lowest=True)
print(f"{IR_SENSOR} bins: {bins}")

# ----------------------------
# STEP 2: COMPUTE CPT FOR IR7
# ----------------------------
bin_col = f"{IR_SENSOR}_bin"
cpt_counts = df.groupby([LABEL_COLUMN, bin_col]).size().unstack(fill_value=0)
cpt = cpt_counts.div(cpt_counts.sum(axis=1), axis=0)
cpt_file = os.path.join(CPT_OUTPUT_DIR, f"CPT_{IR_SENSOR}_vs_{LABEL_COLUMN}.csv")
cpt.to_csv(cpt_file)
print(f"✅ CPT saved: {cpt_file}")
print(cpt, "\n")

# ----------------------------
# STEP 3: SAVE DISCRETIZED CSV
# ----------------------------
df.to_csv(DISCRETIZED_CSV, index=False)
print("Discretized CSV saved:", DISCRETIZED_CSV)
