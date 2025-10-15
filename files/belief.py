import pandas as pd
import os

# ----------------------------
# LOAD CPT FOR IR7 ONLY
# ----------------------------
def load_CPTs(cpt_folder="CPTs"):
    cpt_file = os.path.join(cpt_folder, "CPT_IR7_vs_label.csv")
    if not os.path.exists(cpt_file):
        raise FileNotFoundError(f"{cpt_file} not found.")
    CPTs = {"IR7": pd.read_csv(cpt_file, index_col=0)}
    return CPTs

# ----------------------------
# DISCRETIZE IR7 reading
# ----------------------------
def discretize_IR7(value, thresholds=(0, 50, 150, 1000)):
    if value <= thresholds[1]:
        return "Near"
    elif value <= thresholds[2]:
        return "Medium"
    else:
        return "Far"

# ----------------------------
# BELIEF FUNCTION USING ONLY IR7
# ----------------------------
def belief(sensor_readings, inner_configuration):
    CPTs = inner_configuration
    cpt_IR7 = CPTs["IR7"]
    states = cpt_IR7.index.tolist()  # ['Wall','Door','Door_Passed']
    probs = {state: 1.0 for state in states}

    ir7_value = sensor_readings["IR7"]
    bin_label = discretize_IR7(ir7_value)

    for state in states:
        try:
            prob = cpt_IR7.loc[state, bin_label]
        except KeyError:
            prob = 1e-6  # avoid zero
        probs[state] *= prob

    total = sum(probs.values())
    for state in probs:
        probs[state] /= total

    return probs
