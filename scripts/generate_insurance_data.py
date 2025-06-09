import pandas as pd
import random
from faker import Faker
import os
from datetime import datetime

# Initialize Faker
fake = Faker()

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, "../output")

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Define constants for mock data
claim_statuses = ["pending", "approved", "denied", "closed"]
policy_types = ["auto", "health", "property", "life"]
incident_types = ["accident", "fire", "theft", "medical"]
payment_methods = ["bank_transfer", "check", "credit_card"]
adjuster_departments = ["auto_claims", "health_claims", "property_claims", "life_claims"]

# Generate mock data
data = []
for _ in range(1000):
    policy_holder_name = fake.name()
    policy_id = fake.uuid4()
    claim_id = fake.uuid4()
    claim_date = fake.date_between(start_date="-1y", end_date="today").strftime("%Y-%m-%d")
    claim_date_dt = datetime.strptime(claim_date, "%Y-%m-%d")
    incident_date = fake.date_between(start_date="-2y", end_date=claim_date_dt).strftime("%Y-%m-%d")
    claim_amount = round(random.uniform(500, 50000), 2)  # Claim amount between $500 and $50,000
    approved_amount = round(random.uniform(0, claim_amount), 2)
    claim_status = random.choice(claim_statuses)
    policy_type = random.choice(policy_types)
    incident_type = random.choice(incident_types)
    incident_location = fake.address()
    adjuster_name = fake.name()
    adjuster_id = fake.uuid4()
    adjuster_department = random.choice(adjuster_departments)
    fraud_flag = random.choice(["yes", "no"])
    deductible_amount = round(random.uniform(100, 5000), 2)
    payout_amount = max(0, approved_amount - deductible_amount) if approved_amount > deductible_amount else 0
    payment_date = fake.date_between(start_date=claim_date_dt, end_date="today").strftime("%Y-%m-%d") if payout_amount > 0 else "0000-00-00"
    payment_method = random.choice(payment_methods) if payout_amount > 0 else "none"
    notes = fake.sentence()

    # Append row to data
    data.append([
        policy_holder_name, policy_id, claim_id, claim_date, incident_date, claim_amount, approved_amount,
        claim_status, policy_type, incident_type, incident_location, adjuster_name, adjuster_id,
        adjuster_department, fraud_flag, deductible_amount, payout_amount, payment_date,
        payment_method, notes
    ])

# Create DataFrame
columns = [
    "policy_holder_name", "policy_id", "claim_id", "claim_date", "incident_date", "claim_amount",
    "approved_amount", "claim_status", "policy_type", "incident_type", "incident_location",
    "adjuster_name", "adjuster_id", "adjuster_department", "fraud_flag", "deductible_amount",
    "payout_amount", "payment_date", "payment_method", "notes"
]
df = pd.DataFrame(data, columns=columns)

# Generate file name with current date
current_date = datetime.now()
file_name = f"insurance_claims_{current_date.strftime('%m-%d')}.csv"
output_path = os.path.join(output_dir, file_name)

# Save to CSV
df.to_csv(output_path, index=False)

# Output file name
print(f"Mock data generated and saved to {output_path}")

# Created/Modified files during execution:
print(f"Created file: {output_path}")
