import pandas as pd
import numpy as np
import os

os.makedirs("data", exist_ok=True)

np.random.seed(42)
TOTAL_CLAIMS = 100

mock_data = {
    "claim_id": [f"CLM-{1000 + i}" for i in range(TOTAL_CLAIMS)],
    "policy_id": [f"POL-{5000 + np.random.randint(1000, 9900)}" for i in range(TOTAL_CLAIMS)],
    "claim_amount": np.random.randint(2000, 45000, size=TOTAL_CLAIMS),
    "months_as_customer": np.random.randint(1, 120, size=TOTAL_CLAIMS),
    "incident_type": np.random.choice(["Parked Car Damage", "Single Vehicle Collision", "Multi-Vehicle Collision", "Theft"], size=TOTAL_CLAIMS),
    "police_report_available": np.random.choice(["Yes", "No"], size=TOTAL_CLAIMS, p=[0.65, 0.35]),
    "fraud_probability": np.round(np.random.uniform(0.01, 0.95, size=TOTAL_CLAIMS), 3)
}

df = pd.DataFrame(mock_data)
df.to_csv("data/insurance_claims_test_dataset.csv", index=False)
print("📦 Successfully created mock dataset at 'data/insurance_claims_test_dataset.csv'!")
