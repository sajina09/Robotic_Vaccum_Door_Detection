import os
import pandas as pd
import pickle
import json
import numpy as np

CPT_DIR = "CPTs"
OUTPUT_MODEL = os.path.join(CPT_DIR, "sensor_fusion_model.pkl")
BIN_JSON = os.path.join(CPT_DIR, "ir_bin_edges.json")
DISCRETIZED_CSV = "robot_sensor_data_discretized.csv"

# --------------------------------------------------
# LOAD DISCRETIZED DATA
# --------------------------------------------------
df = pd.read_csv(DISCRETIZED_CSV)
LABELS = df["Location"].unique().tolist()
IR_SENSORS = [f"IR{i+1}" for i in range(7)]
IR_BIN_LABELS = ["Near", "Medium", "Far"]

print("✅ Loaded:", DISCRETIZED_CSV)
print("Labels:", LABELS)

# --------------------------------------------------
# BUILD MODEL DICTIONARY
# --------------------------------------------------
model = {label: {} for label in LABELS}

for label in LABELS:
    for ir in IR_SENSORS:
        cpt_file = os.path.join(CPT_DIR, f"CPT_{ir}_vs_Location.csv")
        if not os.path.exists(cpt_file):
            raise FileNotFoundError(f"Missing CPT file: {cpt_file}")

        cpt_df = pd.read_csv(cpt_file, index_col=0)

        # normalize rows again just in case
        cpt_df = cpt_df.div(cpt_df.sum(axis=1), axis=0)

        if label in cpt_df.index:
            probs = cpt_df.loc[label, IR_BIN_LABELS].values
        else:
            probs = [1/3, 1/3, 1/3]  # fallback uniform

        model[label][ir] = probs.tolist()

# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------
with open(OUTPUT_MODEL, "wb") as f:
    pickle.dump(model, f)
print("✅ Saved:", OUTPUT_MODEL)

# --------------------------------------------------
# SAVE BIN EDGES (FROM ORIGINAL CPT STEP)
# --------------------------------------------------
if not os.path.exists(BIN_JSON):
    ir_bins_dict = {}
    for ir in IR_SENSORS:
        vals = df[ir].values
        bins = [
            float(vals.min() - 1),
            float(vals.min() + (vals.max() - vals.min()) / 3),
            float(vals.min() + 2 * (vals.max() - vals.min()) / 3),
            float(vals.max() + 1)
        ]
        ir_bins_dict[ir] = bins

    # ✅ FIX: Convert all numpy/int64 types to native Python float
    ir_bins_dict = {k: [float(x) for x in v] for k, v in ir_bins_dict.items()}

    with open(BIN_JSON, "w") as f:
        json.dump(ir_bins_dict, f, indent=2)
    print("✅ Saved:", BIN_JSON)
else:
    print("✅ Found existing:", BIN_JSON)
