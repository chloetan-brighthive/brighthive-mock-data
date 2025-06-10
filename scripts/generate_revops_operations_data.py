import os
import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import uuid

# Set up Faker and random seed for reproducibility
fake = Faker()
random.seed(42)
Faker.seed(42)

# Output directory
today_str = datetime.now().strftime("%m-%d")
script_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(script_dir, f"../output/revops_{today_str}")
os.makedirs(output_dir, exist_ok=True)

# Helper to write CSV
def write_csv(subdomain, table_name, fieldnames, rows):
    filename = f"{output_dir}/revops_{subdomain}_{table_name}.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"Wrote {filename} with {len(rows)} records")

# Helper function to generate date ranges
def date_range(start_date, end_date, step_days=1):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=step_days)

# 1. BILLING AND INVOICING DATA
def generate_billing_and_invoicing_data(n_customers=4000):
    fieldnames = [
        'invoice_id', 'customer_id', 'invoice_date', 'due_date', 'amount', 
        'payment_date', 'payment_method', 'payment_terms', 'collection_status'
    ]
    
    payment_methods = ['Credit Card', 'ACH', 'Wire Transfer', 'Check', 'PayPal']
    payment_terms = ['Net 15', 'Net 30', 'Net 45', 'Net 60', 'Due on Receipt']
    collection_statuses = ['Paid', 'Pending', 'Overdue', 'In Collection', 'Written Off']
    
    rows = []
    invoice_id = 1
    
    # Generate invoices over 3 years
    start_date = datetime.now().date() - timedelta(days=3*365)
    end_date = datetime.now().date()
    
    for customer_id in range(1, n_customers + 1):
        # Customer start date
        customer_start = fake.date_between(start_date=start_date, end_date=end_date)
        
        # Generate monthly invoices from customer start
        current_date = customer_start.replace(day=1)  # Start of month
        
        # Base invoice amount varies by customer
        base_amount = random.uniform(1000, 50000)
        
        while current_date <= end_date:
            # Monthly invoice with some variation
            invoice_amount = base_amount * random.uniform(0.8, 1.2)
            
            # Invoice date (typically first of month)
            invoice_date = current_date
            
            # Payment terms
            terms = random.choices(payment_terms, weights=[0.1, 0.6, 0.2, 0.08, 0.02])[0]
            
            # Due date based on terms
            if terms == 'Due on Receipt':
                due_date = invoice_date
            elif terms == 'Net 15':
                due_date = invoice_date + timedelta(days=15)
            elif terms == 'Net 30':
                due_date = invoice_date + timedelta(days=30)
            elif terms == 'Net 45':
                due_date = invoice_date + timedelta(days=45)
            else:  # Net 60
                due_date = invoice_date + timedelta(days=60)
            
            # Payment behavior
            if due_date <= datetime.now().date():
                # Invoice is due, determine if paid
                if random.random() < 0.85:  # 85% pay on time or late
                    # Payment date (some pay early, some late)
                    payment_delay = random.randint(-5, 30)  # -5 to 30 days from due date
                    payment_date = due_date + timedelta(days=payment_delay)
                    
                    if payment_date <= datetime.now().date():
                        if payment_delay <= 0:
                            status = 'Paid'
                        elif payment_delay <= 30:
                            status = 'Paid'
                        else:
                            status = 'Overdue'
                    else:
                        status = 'Pending'
                else:
                    # Unpaid invoices
                    days_overdue = (datetime.now().date() - due_date).days
                    if days_overdue <= 30:
                        status = 'Overdue'
                        payment_date = ''
                    elif days_overdue <= 90:
                        status = 'In Collection'
                        payment_date = ''
                    else:
                        status = random.choices(['In Collection', 'Written Off'], weights=[0.7, 0.3])[0]
                        payment_date = ''
            else:
                # Future invoice
                status = 'Pending'
                payment_date = ''
            
            rows.append({
                'invoice_id': invoice_id,
                'customer_id': customer_id,
                'invoice_date': invoice_date.strftime('%Y-%m-%d'),
                'due_date': due_date.strftime('%Y-%m-%d'),
                'amount': round(invoice_amount, 2),
                'payment_date': payment_date.strftime('%Y-%m-%d') if payment_date else '',
                'payment_method': random.choice(payment_methods) if payment_date else '',
                'payment_terms': terms,
                'collection_status': status
            })
            
            invoice_id += 1
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
            
            # Slight growth in invoice amount over time
            base_amount *= random.uniform(1.0, 1.02)
    
    write_csv('financial', 'billing_and_invoicing', fieldnames, rows)
    return rows

# 2. FORECASTING DATA
def generate_forecasting_data(n_reps=50):
    fieldnames = [
        'forecast_id', 'sales_rep_id', 'period', 'quota', 'pipeline_value', 
        'forecast_amount', 'probability_weighted_forecast', 'quota_attainment'
    ]
    
    rows = []
    forecast_id = 1
    
    # Generate monthly forecasts for 3 years
    start_date = datetime.now().date() - timedelta(days=3*365)
    end_date = datetime.now().date()
    
    for rep_id in range(1, n_reps + 1):
        # Rep's base quota (annual, will be divided by 12 for monthly)
        annual_quota = random.uniform(500000, 2000000)
        monthly_quota = annual_quota / 12
        
        # Generate monthly forecasts
        current_date = start_date.replace(day=1)  # Start of month
        
        while current_date <= end_date:
            # Pipeline value varies throughout the month/quarter
            pipeline_multiplier = random.uniform(1.5, 4.0)  # Pipeline typically 1.5-4x quota
            pipeline_value = monthly_quota * pipeline_multiplier
            
            # Forecast amount (what rep thinks they'll close)
            forecast_confidence = random.uniform(0.6, 1.2)
            forecast_amount = monthly_quota * forecast_confidence
            
            # Probability weighted forecast (more conservative)
            prob_weighted = forecast_amount * random.uniform(0.7, 0.9)
            
            # Quota attainment (for past periods only)
            if current_date < datetime.now().date().replace(day=1):
                # Historical performance
                attainment = random.uniform(0.4, 1.5)  # 40% to 150% of quota
                actual_quota_attainment = round(attainment, 3)
            else:
                # Future periods - no attainment yet
                actual_quota_attainment = ''
            
            # Period string
            period = current_date.strftime('%Y-%m')
            
            rows.append({
                'forecast_id': forecast_id,
                'sales_rep_id': rep_id,
                'period': period,
                'quota': round(monthly_quota, 2),
                'pipeline_value': round(pipeline_value, 2),
                'forecast_amount': round(forecast_amount, 2),
                'probability_weighted_forecast': round(prob_weighted, 2),
                'quota_attainment': actual_quota_attainment
            })
            
            forecast_id += 1
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
                # Annual quota adjustment
                annual_quota *= random.uniform(1.05, 1.15)  # 5-15% growth
                monthly_quota = annual_quota / 12
            else:
                current_date = current_date.replace(month=current_date.month + 1)
    
    write_csv('financial', 'forecasting', fieldnames, rows)
    return rows

# 3. TERRITORY AND CAPACITY PLANNING
def generate_territory_planning_data(n_reps=50):
    fieldnames = [
        'territory_id', 'sales_rep_id', 'territory_name', 'market_size', 
        'accounts_assigned', 'quota_assigned', 'productivity_score', 'coverage_ratio'
    ]
    
    territory_types = ['North America East', 'North America West', 'EMEA', 'APAC', 'LATAM', 
                      'Enterprise', 'Mid-Market', 'SMB', 'Federal', 'Healthcare']
    
    rows = []
    territory_id = 1
    
    # Generate quarterly territory data for 3 years
    start_date = datetime.now().date() - timedelta(days=3*365)
    end_date = datetime.now().date()
    
    for rep_id in range(1, n_reps + 1):
        # Rep's territory assignment
        territory_name = f"{random.choice(territory_types)} - {fake.state()}"
        
        # Base territory characteristics
        base_market_size = random.uniform(10000000, 100000000)  # $10M - $100M market
        base_accounts = random.randint(50, 500)
        base_quota = random.uniform(500000, 2000000)
        
        # Generate quarterly data
        current_date = start_date
        quarter = 1
        
        while current_date <= end_date:
            # Market size grows over time
            market_size = base_market_size * (1 + (current_date.year - start_date.year) * 0.1)
            
            # Accounts assigned (can change quarterly)
            accounts_assigned = base_accounts + random.randint(-20, 20)
            
            # Quota assigned (grows annually)
            years_elapsed = (current_date.year - start_date.year)
            quota_assigned = base_quota * (1.1 ** years_elapsed)  # 10% annual growth
            
            # Productivity score (0-100, based on performance)
            productivity_score = random.uniform(60, 95)
            
            # Coverage ratio (accounts covered / total addressable accounts)
            total_addressable = market_size / 50000  # Assume $50K average account size
            coverage_ratio = min(1.0, accounts_assigned / total_addressable)
            
            rows.append({
                'territory_id': territory_id,
                'sales_rep_id': rep_id,
                'territory_name': territory_name,
                'market_size': round(market_size, 2),
                'accounts_assigned': accounts_assigned,
                'quota_assigned': round(quota_assigned, 2),
                'productivity_score': round(productivity_score, 1),
                'coverage_ratio': round(coverage_ratio, 3)
            })
            
            territory_id += 1
            
            # Move to next quarter
            current_date += timedelta(days=90)
            quarter += 1
    
    write_csv('financial', 'territory_planning', fieldnames, rows)
    return rows

# 4. COMPENSATION DATA
def generate_compensation_data(n_reps=50):
    fieldnames = [
        'comp_id', 'sales_rep_id', 'period', 'base_salary', 'commission_earned', 
        'quota_achievement', 'accelerator_rate', 'total_compensation'
    ]
    
    rows = []
    comp_id = 1
    
    # Generate monthly compensation data for 3 years
    start_date = datetime.now().date() - timedelta(days=3*365)
    end_date = datetime.now().date()
    
    for rep_id in range(1, n_reps + 1):
        # Rep's compensation structure
        annual_base_salary = random.uniform(80000, 150000)
        monthly_base = annual_base_salary / 12
        
        # Commission structure
        base_commission_rate = random.uniform(0.02, 0.08)  # 2-8% of sales
        
        # Generate monthly compensation
        current_date = start_date.replace(day=1)
        
        while current_date <= end_date:
            # Only calculate for past periods
            if current_date < datetime.now().date().replace(day=1):
                # Quota achievement for the month
                quota_achievement = random.uniform(0.3, 1.8)  # 30% to 180%
                
                # Commission calculation
                monthly_quota = random.uniform(40000, 150000)  # Monthly quota
                actual_sales = monthly_quota * quota_achievement
                
                # Base commission
                commission_earned = actual_sales * base_commission_rate
                
                # Accelerator (bonus for over-achievement)
                accelerator_rate = 1.0
                if quota_achievement > 1.0:
                    # Accelerated commission for over-achievement
                    over_achievement = quota_achievement - 1.0
                    accelerator_rate = 1.0 + (over_achievement * 0.5)  # 50% accelerator
                    commission_earned *= accelerator_rate
                
                total_compensation = monthly_base + commission_earned
                
            else:
                # Future periods - no data yet
                quota_achievement = ''
                commission_earned = 0
                accelerator_rate = ''
                total_compensation = monthly_base
            
            period = current_date.strftime('%Y-%m')
            
            rows.append({
                'comp_id': comp_id,
                'sales_rep_id': rep_id,
                'period': period,
                'base_salary': round(monthly_base, 2),
                'commission_earned': round(commission_earned, 2) if commission_earned else 0,
                'quota_achievement': round(quota_achievement, 3) if quota_achievement else '',
                'accelerator_rate': round(accelerator_rate, 3) if accelerator_rate != '' else '',
                'total_compensation': round(total_compensation, 2)
            })
            
            comp_id += 1
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
                # Annual salary adjustment
                annual_base_salary *= random.uniform(1.02, 1.08)  # 2-8% annual increase
                monthly_base = annual_base_salary / 12
            else:
                current_date = current_date.replace(month=current_date.month + 1)
    
    write_csv('financial', 'compensation', fieldnames, rows)
    return rows

# MAIN EXECUTION FOR FINANCIAL & OPERATIONAL DATA
def generate_financial_operational_data():
    print("Generating Financial & Operational Data...")
    print("=" * 60)
    
    # Generate all financial & operational tables
    billing_and_invoicing = generate_billing_and_invoicing_data(4000)
    forecasting = generate_forecasting_data(50)
    territory_planning = generate_territory_planning_data(50)
    compensation = generate_compensation_data(50)
    
    print("=" * 60)
    print("Financial & Operational data generation complete!")
    print(f"Output directory: {output_dir}")

# Execute the generation
if __name__ == "__main__":
    generate_financial_operational_data()