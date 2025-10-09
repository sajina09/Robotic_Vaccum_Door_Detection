# sample_run.py
from belief import SensorFusion
import os
import csv

# Initialize sensor fusion
sf = SensorFusion(cpt_dir="CPTs")

# Example sensor readings (replace with real robot readings)
sensor_data_samples = [
    {'IR1':320,'IR2':400,'IR3':200,'IR4':300,'IR5':450,'IR6':500,'IR7':150},
    {'IR1':100,'IR2':150,'IR3':200,'IR4':300,'IR5':400,'IR6':500,'IR7':600}
]

# Create output folder
os.makedirs("outputs", exist_ok=True)

# Write belief maps to CSV
output_file = "outputs/belief_output.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.writer(f)
    headers = ["Sample", "Wall", "Door_Start", "Door", "Door_Passed"]
    writer.writerow(headers)
    
    for i, sample in enumerate(sensor_data_samples):
        belief_map = sf.belief(sample)
        writer.writerow([i+1] + [belief_map.get(label, 0) for label in ["Wall","Door_Start","Door","Door_Passed"]])
        print(f"Sample {i+1}: {belief_map}")

print(f"✅ Belief CSV generated: {output_file}")
