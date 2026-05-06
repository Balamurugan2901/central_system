import pandas as pd
import numpy as np
import random
from pathlib import Path

def generate_synthetic_data(num_samples: int = 5000):
    np.random.seed(42)
    random.seed(42)

    data = []

    # Attack types and their corresponding autonomous action
    scenarios = [
        # Normal Traffic (ALLOW)
        {"weight": 0.6, "event": "Normal", "action": "ALLOW",
         "packet_rate_range": (5, 30), "failed_logins_range": (0, 1)},
        
        # Minor Anomaly / Scan (ALERT)
        {"weight": 0.15, "event": "Port Scan", "action": "ALERT",
         "packet_rate_range": (30, 80), "failed_logins_range": (0, 2)},
        
        # Brute Force (BLOCK_IP)
        {"weight": 0.15, "event": "Brute Force", "action": "BLOCK_IP",
         "packet_rate_range": (10, 50), "failed_logins_range": (4, 15)},
        
        # DDoS (RATE_LIMIT)
        {"weight": 0.10, "event": "DDoS", "action": "RATE_LIMIT",
         "packet_rate_range": (200, 1000), "failed_logins_range": (0, 0)}
    ]

    for _ in range(num_samples):
        # Pick a scenario based on weights
        weights = [s["weight"] for s in scenarios]
        scenario = random.choices(scenarios, weights=weights)[0]

        packet_rate = np.random.uniform(scenario["packet_rate_range"][0], scenario["packet_rate_range"][1])
        failed_logins = np.random.randint(scenario["failed_logins_range"][0], scenario["failed_logins_range"][1] + 1)
        
        data.append({
            "packet_rate": round(packet_rate, 2),
            "failed_logins": failed_logins,
            "event": scenario["event"],
            "action_label": scenario["action"]
        })

    df = pd.DataFrame(data)
    
    # Save the expanded dataset
    output_path = Path("models/synthetic_intrusion_dataset.csv")
    df.to_csv(output_path, index=False)
    
    print(f"✅ Generated {num_samples} samples and saved to {output_path}")
    print("\nClass distribution:")
    print(df["action_label"].value_counts())

if __name__ == "__main__":
    generate_synthetic_data()
