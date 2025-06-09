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
output_dir = os.path.join(script_dir, f"../output/finance_banking_{date_suffix}")
os.makedirs(output_dir, exist_ok=True)

def generate_customer_profiles(n_customers=100):
    account_types = ['Savings', 'Checking', 'Business']
    risk_categories = ['Low', 'Medium', 'High']

    customers = []
    for i in range(n_customers):
        name = fake.name()
        email = f"{name.lower().replace(' ', '.')}{random.randint(1,999)}@{fake.domain_name()}"
        customers.append({
            'customer_id': f'CUS{i+1:04d}',
            'name': name,
            'age': random.randint(18, 80),
            'gender': random.choice(['M', 'F']),
            'address': fake.address().replace('\n', ', '),
            'phone': fake.phone_number(),
            'email': email,
            'account_type': random.choice(account_types),
            'account_balance': round(random.uniform(1000, 100000), 2),
            'credit_score': random.randint(300, 850),
            'risk_category': random.choice(risk_categories)
        })
    return pd.DataFrame(customers)

def generate_transactions(n_transactions=1000, n_customers=100):
    transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment']
    channels = ['Online', 'ATM', 'Branch', 'Mobile']
    statuses = ['Completed', 'Pending', 'Failed']

    transactions = []
    for i in range(n_transactions):
        amount = round(random.uniform(10, 5000), 2)
        transactions.append({
            'transaction_id': f'TRX{i+1:06d}',
            'customer_id': f'CUS{random.randint(1, n_customers):04d}',
            'transaction_date': fake.date_time_between(start_date='-30d', end_date='now'),
            'transaction_type': random.choice(transaction_types),
            'amount': amount,
            'account_balance_after_transaction': round(random.uniform(amount, 100000), 2),
            'channel': random.choice(channels),
            'status': random.choice(statuses)
        })
    return pd.DataFrame(transactions)

def generate_loans(n_loans=200, n_customers=100):
    loan_types = ['Personal', 'Mortgage', 'Auto', 'Business']
    approval_statuses = ['Approved', 'Rejected', 'Pending']
    repayment_statuses = ['On Track', 'Delinquent', 'Paid Off']

    loans = []
    for i in range(n_loans):
        loans.append({
            'loan_id': f'LN{i+1:04d}',
            'customer_id': f'CUS{random.randint(1, n_customers):04d}',
            'loan_type': random.choice(loan_types),
            'loan_amount': round(random.uniform(5000, 500000), 2),
            'interest_rate': round(random.uniform(3, 15), 2),
            'loan_term_years': random.randint(1, 30),
            'approval_status': random.choice(approval_statuses),
            'disbursement_date': fake.date_between(start_date='-2y', end_date='today'),
            'repayment_status': random.choice(repayment_statuses)
        })
    return pd.DataFrame(loans)

def generate_credit_risk_assessments(n_assessments=100, n_customers=100):
    risk_categories = ['Low', 'Medium', 'High']
    recommendations = ['Approve', 'Decline', 'Review']

    assessments = []
    for i in range(n_assessments):
        assessments.append({
            'assessment_id': f'ASM{i+1:04d}',
            'customer_id': f'CUS{random.randint(1, n_customers):04d}',
            'credit_score': random.randint(300, 850),
            'debt_to_income_ratio': round(random.uniform(0.1, 0.6), 2),
            'loan_to_value_ratio': round(random.uniform(0.5, 0.9), 2),
            'risk_category': random.choice(risk_categories),
            'assessment_date': fake.date_between(start_date='-60d', end_date='today'),
            'recommendation': random.choice(recommendations)
        })
    return pd.DataFrame(assessments)

def generate_fraud_alerts(n_alerts=50, n_transactions=1000):
    alert_types = ['Unusual Location', 'Large Transaction', 'Multiple Failed Logins',
                  'Suspicious Pattern', 'Unknown Device']
    alert_statuses = ['Investigating', 'Resolved', 'False Positive']

    alerts = []
    for i in range(n_alerts):
        alert_date = fake.date_time_between(start_date='-30d', end_date='now')
        alerts.append({
            'alert_id': f'ALT{i+1:04d}',
            'transaction_id': f'TRX{random.randint(1, n_transactions):06d}',
            'customer_id': f'CUS{random.randint(1, 100):04d}',
            'alert_date': alert_date,
            'alert_type': random.choice(alert_types),
            'alert_status': random.choice(alert_statuses),
            'resolution_date': fake.date_time_between(start_date=alert_date, end_date='now')
        })
    return pd.DataFrame(alerts)

def generate_financial_performance(n_days=30):
    performance = []
    start_date = datetime.now() - timedelta(days=n_days)

    for i in range(n_days):
        current_date = start_date + timedelta(days=i)
        total_revenue = random.uniform(100000, 500000)
        total_expenses = random.uniform(50000, 400000)
        net_profit = total_revenue - total_expenses

        performance.append({
            'performance_id': f'PER{i+1:04d}',
            'date': current_date,
            'total_revenue': round(total_revenue, 2),
            'total_expenses': round(total_expenses, 2),
            'net_profit': round(net_profit, 2),
            'profit_margin': round(net_profit / total_revenue * 100, 2),
            'key_performance_indicator': round(random.uniform(0.5, 2.5), 2)
        })
    return pd.DataFrame(performance)

# Generate all datasets
customer_df = generate_customer_profiles()
transactions_df = generate_transactions()
loans_df = generate_loans()
credit_risk_df = generate_credit_risk_assessments()
fraud_alerts_df = generate_fraud_alerts()
performance_df = generate_financial_performance()

# Save all datasets
datasets = {
    'customer_profiles': customer_df,
    'transactions': transactions_df,
    'loans': loans_df,
    'credit_risk_assessments': credit_risk_df,
    'fraud_detection_alerts': fraud_alerts_df,
    'financial_performance': performance_df
}

# Save files and print information
for name, df in datasets.items():
    filename = f'finance_banking_{name}_{date_suffix}.csv'
    filepath = os.path.join(output_dir, filename)
    df.to_csv(filepath, index=False)
    print(f"\nDataset: {name}")
    print(f"Number of records: {len(df)}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"Saved to: {filepath}")

print("\nAll datasets have been generated and saved successfully!")