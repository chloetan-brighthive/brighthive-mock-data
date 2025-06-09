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
output_dir = os.path.join(script_dir, f"../output/healthcare_{date_suffix}")
os.makedirs(output_dir, exist_ok=True)

def generate_medical_staff(n_staff=50):
    roles = ['Doctor', 'Nurse', 'Admin', 'Technician', 'Specialist']
    departments = ['Cardiology', 'Pediatrics', 'Emergency', 'Surgery', 'Oncology', 'General Medicine']
    specializations = {
        'Doctor': ['Cardiologist', 'Pediatrician', 'Emergency Physician', 'Surgeon', 'Oncologist', 'General Physician'],
        'Nurse': ['RN', 'LPN', 'Nurse Practitioner', 'Clinical Nurse', 'Emergency Nurse'],
        'Admin': ['Reception', 'Billing', 'Records', 'HR', 'Operations'],
        'Technician': ['Lab', 'Radiology', 'Pharmacy', 'Equipment', 'IT'],
        'Specialist': ['Physiotherapist', 'Nutritionist', 'Psychologist', 'Radiologist', 'Anesthesiologist']
    }

    staff = []
    for i in range(n_staff):
        role = random.choice(roles)
        staff.append({
            'staff_id': f'STF{i+1:03d}',
            'name': fake.name(),
            'role': role,
            'specialization': random.choice(specializations[role]),
            'department': random.choice(departments),
            'phone': fake.phone_number(),
            'email': fake.email(),
            'hire_date': fake.date_between(start_date='-5y', end_date='today'),
            'shift_schedule': random.choice(['Morning', 'Afternoon', 'Night', 'Rotating'])
        })
    return pd.DataFrame(staff)

def generate_patient_records(n_patients=100):
    medical_conditions = ['Hypertension', 'Diabetes', 'Asthma', 'Arthritis', 'None', 'Heart Disease']
    allergies = ['Penicillin', 'Pollen', 'None', 'Latex', 'Peanuts', 'Shellfish']

    patients = []
    for i in range(n_patients):
        name = fake.name()
        email = f"{name.lower().replace(' ', '.')}{random.randint(1,999)}@{random.choice(['gmail.com', 'yahoo.com', 'hotmail.com'])}"
        patients.append({
            'patient_id': f'PAT{i+1:03d}',
            'name': name,
            'age': random.randint(18, 90),
            'gender': random.choice(['M', 'F']),
            'address': fake.address().replace('\n', ', '),
            'phone': fake.phone_number(),
            'email': email,
            'date_of_birth': fake.date_of_birth(minimum_age=18, maximum_age=90),
            'medical_history': random.choice(medical_conditions),
            'allergies': random.choice(allergies),
            'primary_physician': f'STF{random.randint(1,50):03d}',
            'insurance_provider': random.choice(['BlueCross', 'Aetna', 'UnitedHealth', 'Cigna', 'Medicare'])
        })
    return pd.DataFrame(patients)

def generate_appointments(n_appointments=500, patient_df=None, staff_df=None):
    appointment_types = ['Regular Checkup', 'Follow-up', 'Emergency', 'Consultation', 'Procedure']
    statuses = ['Scheduled', 'Completed', 'Cancelled', 'No-show']

    appointments = []
    for i in range(n_appointments):
        patient_id = f'PAT{random.randint(1,100):03d}'
        appointments.append({
            'appointment_id': f'APT{i+1:03d}',
            'patient_id': patient_id,
            'doctor_id': f'STF{random.randint(1,50):03d}',
            'appointment_date': fake.date_between(start_date='-30d', end_date='+30d'),
            'appointment_time': fake.time(),
            'status': random.choice(statuses),
            'reason_for_visit': random.choice(appointment_types),
            'follow_up_required': random.choice([True, False])
        })
    return pd.DataFrame(appointments)

def generate_hospital_performance(n_days=30):
    metrics = []
    start_date = datetime.now() - timedelta(days=n_days)

    for i in range(n_days):
        current_date = start_date + timedelta(days=i)
        metrics.append({
            'metric_id': f'MET{i+1:03d}',
            'date': current_date,
            'bed_occupancy_rate': round(random.uniform(0.60, 0.95), 2),
            'average_wait_time_minutes': random.randint(15, 120),
            'staff_efficiency_score': round(random.uniform(0.70, 0.98), 2)
        })
    return pd.DataFrame(metrics)

def generate_pharmaceutical_inventory(n_items=100):
    categories = ['Medicine', 'Equipment', 'Supplies']
    items = []

    for i in range(n_items):
        items.append({
            'item_id': f'ITM{i+1:03d}',
            'item_name': fake.word() + ' ' + random.choice(['Tablet', 'Injection', 'Syrup', 'Equipment', 'Supply']),
            'category': random.choice(categories),
            'quantity_in_stock': random.randint(0, 1000),
            'reorder_level': random.randint(50, 200),
            'supplier_id': f'SUP{random.randint(1,10):03d}',
            'expiration_date': fake.date_between(start_date='today', end_date='+2y'),
            'unit_price': round(random.uniform(10, 1000), 2)
        })
    return pd.DataFrame(items)

def generate_billing_payments(n_bills=500):
    bills = []

    for i in range(n_bills):
        total_amount = round(random.uniform(100, 5000), 2)
        insurance_covered = round(total_amount * random.uniform(0.5, 0.9), 2)
        bills.append({
            'billing_id': f'BIL{i+1:03d}',
            'patient_id': f'PAT{random.randint(1,100):03d}',
            'appointment_id': f'APT{random.randint(1,500):03d}',
            'total_amount': total_amount,
            'insurance_covered_amount': insurance_covered,
            'out_of_pocket_amount': round(total_amount - insurance_covered, 2),
            'payment_status': random.choice(['Paid', 'Pending', 'Overdue']),
            'payment_date': fake.date_between(start_date='-30d', end_date='today')
        })
    return pd.DataFrame(bills)

def generate_regulatory_compliance(n_records=20):
    departments = ['Emergency', 'Surgery', 'Pharmacy', 'Laboratory', 'General']
    audit_types = ['Safety', 'Documentation', 'Infection Control', 'Medicine Storage', 'Staff Training']

    compliance = []
    for i in range(n_records):
        compliance.append({
            'compliance_id': f'COM{i+1:03d}',
            'audit_date': fake.date_between(start_date='-60d', end_date='today'),
            'department': random.choice(departments),
            'audit_type': random.choice(audit_types),
            'findings': fake.text(max_nb_chars=100),
            'corrective_actions': fake.text(max_nb_chars=100),
            'status': random.choice(['Open', 'Closed', 'In Progress'])
        })
    return pd.DataFrame(compliance)

def generate_patient_outcomes(n_outcomes=200):
    diagnoses = ['Hypertension', 'Diabetes', 'Respiratory Infection', 'Fracture', 'Anxiety']
    outcomes = ['Recovered', 'Improved', 'No Change', 'Deteriorated']

    patient_outcomes = []
    for i in range(n_outcomes):
        start_date = fake.date_between(start_date='-60d', end_date='-30d')
        patient_outcomes.append({
            'outcome_id': f'OUT{i+1:03d}',
            'patient_id': f'PAT{random.randint(1,100):03d}',
            'treatment_id': f'TRT{i+1:03d}',
            'diagnosis': random.choice(diagnoses),
            'treatment_start_date': start_date,
            'treatment_end_date': fake.date_between(start_date=start_date, end_date='today'),
            'outcome': random.choice(outcomes),
            'notes': fake.text(max_nb_chars=100)
        })
    return pd.DataFrame(patient_outcomes)

def generate_supply_chain(n_orders=50):
    orders = []
    for i in range(n_orders):
        quantity_ordered = random.randint(10, 100)
        orders.append({
            'order_id': f'ORD{i+1:03d}',
            'supplier_id': f'SUP{random.randint(1,10):03d}',
            'item_id': f'ITM{random.randint(1,100):03d}',
            'order_date': fake.date_between(start_date='-30d', end_date='today'),
            'delivery_date': fake.date_between(start_date='today', end_date='+30d'),
            'quantity_ordered': quantity_ordered,
            'quantity_received': random.randint(0, quantity_ordered),
            'status': random.choice(['Ordered', 'In Transit', 'Delivered', 'Partially Delivered'])
        })
    return pd.DataFrame(orders)

# Generate all datasets
staff_df = generate_medical_staff()
patients_df = generate_patient_records()
appointments_df = generate_appointments()
performance_df = generate_hospital_performance()
inventory_df = generate_pharmaceutical_inventory()
billing_df = generate_billing_payments()
compliance_df = generate_regulatory_compliance()
outcomes_df = generate_patient_outcomes()
supply_chain_df = generate_supply_chain()

# Save all datasets
datasets = {
    'medical_staff': staff_df,
    'patients': patients_df,
    'appointments': appointments_df,
    'hospital_performance': performance_df,
    'pharmaceutical_inventory': inventory_df,
    'billing_and_payments': billing_df,
    'regulatory_compliance': compliance_df,
    'patient_outcomes': outcomes_df,
    'supply_chain': supply_chain_df
}

# Save files and print information
for name, df in datasets.items():
    filename = f'healthcare_data_{name}_{date_suffix}.csv'
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"\nDataset: {name}")
    print(f"Number of records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Saved to: {filepath}")

print("\nAll datasets have been generated and saved successfully!")