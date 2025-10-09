import json
import pickle
import numpy as np
import os

class SensorFusion:
    def __init__(self, cpt_dir="CPTs"):
        # Load CPTs (from DataCollectionMN and CPT.py)
        with open(os.path.join(cpt_dir, "sensor_fusion_model.pkl"), "rb") as f:
            self.model = pickle.load(f)

        with open(os.path.join(cpt_dir, "ir_bin_edges.json"), "r") as f:
            self.ir_bins = json.load(f)

        # Prior (uniform belief)
        self.prior = {
            "Wall": 0.25,
            "Door_Start": 0.25,
            "Door": 0.25,
            "Door_Passed": 0.25
        }

    def _digitize_ir(self, ir_value, sensor_name):
        """Discretize IR reading into bins according to training edges."""
        bins = self.ir_bins[sensor_name]
        return np.digitize(ir_value, bins, right=False)

    def belief(self, ir_dict):
        """
        Compute posterior belief using Bayesian update:
        P(state | sensors) ∝ P(sensors | state) * P(state)
        """
        states = ["Wall", "Door_Start", "Door", "Door_Passed"]

        # 1️⃣ Compute likelihood for each state
        likelihoods = {}
        for state in states:
            likelihood = 1.0
            for ir_name, ir_value in ir_dict.items():
                binned_val = self._digitize_ir(ir_value, ir_name)
                cpt = self.model[state][ir_name]

                # Bound index to CPT length
                if binned_val >= len(cpt):
                    binned_val = len(cpt) - 1

                likelihood *= cpt[binned_val]
            likelihoods[state] = likelihood

        # 2️⃣ Apply Bayes rule: posterior ∝ likelihood * prior
        unnorm_post = {
            s: likelihoods[s] * self.prior[s] for s in states
        }

        total = sum(unnorm_post.values())
        if total == 0:
            posterior = self.prior
        else:
            posterior = {s: unnorm_post[s] / total for s in states}

        # 3️⃣ Update prior for temporal smoothing
        self.prior = posterior

        return posterior
