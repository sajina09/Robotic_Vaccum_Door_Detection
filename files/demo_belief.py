import csv
from belief import belief, load_CPTs

# ----------------------------
# Load CPTs
# ----------------------------
CPTs = load_CPTs("CPTs")

# ----------------------------
# Example sensor readings (only IR7 now)
# ----------------------------
sensor_samples = [
    {"IR7": 28},
    {"IR7": 200},
    {"IR7": 300}
]

# ----------------------------
# Compute beliefs for each sample
# ----------------------------
results = []
for i, sensors in enumerate(sensor_samples):
    b = belief(sensors, CPTs)
    row = {"Sample": i+1, **sensors, **b}
    results.append(row)

# ----------------------------
# Save to CSV for visualization
# ----------------------------
csv_file = "belief_map_output.csv"
keys = results[0].keys()
with open(csv_file, "w", newline="") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(results)

print(f"Belief map saved to {csv_file}")
