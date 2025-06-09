import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from faker import Faker
import os

# Set up Faker and random seeds
fake = Faker()
np.random.seed(42)
random.seed(42)

# Get current date for directory naming
current_date = datetime.now()
date_suffix = current_date.strftime("%m-%d")

# Get script directory and create output directory
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, f"../output/energy_utilities_{date_suffix}")
os.makedirs(output_dir, exist_ok=True)

def generate_energy_consumption(n_records=1000):
    customer_types = ['Residential', 'Commercial', 'Industrial']
    regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West']

    consumption_data = []
    for i in range(n_records):
        customer_type = random.choice(customer_types)
        # Scale consumption based on customer type
        base_consumption = {
            'Residential': (10, 100),
            'Commercial': (100, 1000),
            'Industrial': (1000, 10000)
        }[customer_type]

        consumption_data.append({
            'customer_id': f'CUST{i+1:04d}',
            'customer_type': customer_type,
            'region': random.choice(regions),
            'date': fake.date_between(start_date='-30d', end_date='today'),
            'energy_consumed_kwh': round(random.uniform(*base_consumption), 2),
            'peak_usage_kwh': round(random.uniform(base_consumption[0]*0.6, base_consumption[1]*0.6), 2),
            'off_peak_usage_kwh': round(random.uniform(base_consumption[0]*0.4, base_consumption[1]*0.4), 2),
            'billing_amount': round(random.uniform(base_consumption[0]*0.15, base_consumption[1]*0.15), 2)
        })
    return pd.DataFrame(consumption_data)

def generate_energy_production(n_records=500):
    plant_types = ['Solar', 'Wind', 'Hydro', 'Fossil Fuel']
    regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West']

    production_data = []
    for i in range(n_records):
        plant_type = random.choice(plant_types)
        production_data.append({
            'plant_id': f'PLT{i+1:04d}',
            'plant_type': plant_type,
            'region': random.choice(regions),
            'date': fake.date_between(start_date='-30d', end_date='today'),
            'energy_produced_kwh': round(random.uniform(5000, 50000), 2),
            'capacity_utilization': round(random.uniform(0.5, 0.95), 2),
            'emissions_tonnes': round(random.uniform(0, 100), 2) if plant_type == 'Fossil Fuel' else 0
        })
    return pd.DataFrame(production_data)

def generate_outage_reports(n_records=200):
    causes = ['Weather', 'Equipment Failure', 'Maintenance', 'Animal Contact', 'Vehicle Accident']
    regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West']
    statuses = ['Resolved', 'Ongoing']

    outage_data = []
    for i in range(n_records):
        start_date = fake.date_time_between(start_date='-30d', end_date='now')
        duration = random.randint(30, 480)  # 30 mins to 8 hours
        end_date = start_date + timedelta(minutes=duration) if random.random() > 0.1 else None

        outage_data.append({
            'outage_id': f'OUT{i+1:04d}',
            'customer_id': f'CUST{random.randint(1, 1000):04d}',
            'region': random.choice(regions),
            'outage_start': start_date,
            'outage_end': end_date,
            'duration_minutes': duration if end_date else None,
            'cause': random.choice(causes),
            'status': 'Resolved' if end_date else 'Ongoing'
        })
    return pd.DataFrame(outage_data)

# Generate datasets
consumption_df = generate_energy_consumption()
production_df = generate_energy_production()
outage_df = generate_outage_reports()

# Save datasets
datasets = {
    'energy_consumption': consumption_df,
    'energy_production': production_df,
    'outage_reports': outage_df
}

# Save files and print information
for name, df in datasets.items():
    filename = f'energy_utilities_{name}_{date_suffix}.csv'
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"\nDataset: {name}")
    print(f"Number of records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Saved to: {filepath}")

print("\nAll datasets have been generated and saved successfully!")