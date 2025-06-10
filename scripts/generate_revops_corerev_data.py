import os
import csv
import random
from datetime import datetime, timedelta
from faker import Faker

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

# 1. ACCOUNTS TABLE
def generate_accounts(n=5000):
    fieldnames = [
        'account_id', 'account_name', 'industry', 'company_size', 'annual_revenue',
        'country', 'state', 'city', 'account_type', 'created_date', 'last_modified_date'
    ]
    
    industries = ['Software', 'Finance', 'Healthcare', 'Retail', 'Manufacturing', 
                 'Education', 'Real Estate', 'Media', 'Consulting', 'Technology']
    account_types = ['Customer', 'Prospect', 'Partner', 'Reseller']
    company_sizes = ['Small (1-50)', 'Medium (51-200)', 'Large (201-1000)', 'Enterprise (1000+)']
    
    rows = []
    for i in range(1, n+1):
        created = fake.date_between(start_date='-3y', end_date='today')
        last_mod = fake.date_between(start_date=created, end_date='today')
        
        # Weight account types - more customers and prospects
        account_type = random.choices(account_types, weights=[0.4, 0.35, 0.15, 0.1])[0]
        
        rows.append({
            'account_id': i,
            'account_name': fake.company(),
            'industry': random.choice(industries),
            'company_size': random.choice(company_sizes),
            'annual_revenue': random.randint(500_000, 500_000_000),
            'country': fake.country(),
            'state': fake.state() if random.random() < 0.7 else '',  # 70% have state
            'city': fake.city(),
            'account_type': account_type,
            'created_date': created.strftime('%Y-%m-%d'),
            'last_modified_date': last_mod.strftime('%Y-%m-%d')
        })
    
    write_csv('core', 'accounts', fieldnames, rows)
    return rows

# 2. CONTACTS TABLE
def generate_contacts(accounts, avg_contacts_per_account=5):
    fieldnames = [
        'contact_id', 'account_id', 'first_name', 'last_name', 'email', 'phone',
        'job_title', 'department', 'seniority_level', 'created_date', 'last_activity_date'
    ]
    
    departments = ['Sales', 'Marketing', 'IT', 'Finance', 'HR', 'Operations', 'Legal', 'Product']
    seniority_levels = ['Entry', 'Senior', 'Manager', 'Director', 'VP', 'C-Level']
    job_titles = ['Account Manager', 'Sales Director', 'Marketing Manager', 'IT Director', 
                 'CFO', 'CEO', 'VP Sales', 'Product Manager', 'Operations Manager']
    
    rows = []
    contact_id = 1
    
    for account in accounts:
        # Vary number of contacts per account (1-10, weighted toward 3-7)
        num_contacts = random.choices(range(1, 11), weights=[1,2,4,6,8,6,4,2,1,1])[0]
        
        for _ in range(num_contacts):
            created = fake.date_between(
                start_date=datetime.strptime(account['created_date'], '%Y-%m-%d').date(),
                end_date='today'
            )
            last_activity = fake.date_between(start_date=created, end_date='today')
            
            first_name = fake.first_name()
            last_name = fake.last_name()
            
            rows.append({
                'contact_id': contact_id,
                'account_id': account['account_id'],
                'first_name': first_name,
                'last_name': last_name,
                'email': f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}",
                'phone': fake.phone_number(),
                'job_title': random.choice(job_titles),
                'department': random.choice(departments),
                'seniority_level': random.choice(seniority_levels),
                'created_date': created.strftime('%Y-%m-%d'),
                'last_activity_date': last_activity.strftime('%Y-%m-%d')
            })
            contact_id += 1
    
    write_csv('core', 'contacts', fieldnames, rows)
    return rows

# 3. LEADS TABLE
def generate_leads(n=75000):
    fieldnames = [
        'lead_id', 'first_name', 'last_name', 'email', 'phone', 'company',
        'job_title', 'lead_source', 'lead_status', 'created_date', 'converted_date', 'converted_contact_id'
    ]
    
    lead_sources = ['Website', 'Event', 'Referral', 'Cold Call', 'Partner', 'Social Media', 
                   'Email Campaign', 'Webinar', 'Trade Show', 'Content Download']
    lead_statuses = ['New', 'Working', 'Qualified', 'Unqualified', 'Converted', 'Recycled']
    job_titles = ['Manager', 'Director', 'VP', 'Analyst', 'Coordinator', 'Specialist', 'Executive']
    
    rows = []
    converted_contact_counter = 1
    
    for i in range(1, n+1):
        created = fake.date_between(start_date='-3y', end_date='today')
        
        # Weight lead statuses realistically
        status = random.choices(lead_statuses, weights=[0.25, 0.30, 0.15, 0.20, 0.08, 0.02])[0]
        
        converted_date = ''
        converted_contact_id = ''
        
        if status == 'Converted':
            converted_date = fake.date_between(start_date=created, end_date='today').strftime('%Y-%m-%d')
            converted_contact_id = converted_contact_counter
            converted_contact_counter += 1
        
        first_name = fake.first_name()
        last_name = fake.last_name()
        
        rows.append({
            'lead_id': i,
            'first_name': first_name,
            'last_name': last_name,
            'email': f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}",
            'phone': fake.phone_number(),
            'company': fake.company(),
            'job_title': f"{random.choice(job_titles)} {fake.job()}",
            'lead_source': random.choice(lead_sources),
            'lead_status': status,
            'created_date': created.strftime('%Y-%m-%d'),
            'converted_date': converted_date,
            'converted_contact_id': converted_contact_id
        })
    
    write_csv('core', 'leads', fieldnames, rows)
    return rows

# 4. OPPORTUNITIES TABLE
def generate_opportunities(accounts, contacts, n=15000):
    fieldnames = [
        'opportunity_id', 'account_id', 'contact_id', 'opportunity_name', 'stage', 
        'amount', 'probability', 'close_date', 'created_date', 'last_modified_date', 
        'sales_rep_id', 'lead_source'
    ]
    
    stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    stage_probabilities = {'Prospecting': 10, 'Qualification': 25, 'Proposal': 50, 
                          'Negotiation': 75, 'Closed Won': 100, 'Closed Lost': 0}
    lead_sources = ['Website', 'Event', 'Referral', 'Cold Call', 'Partner', 'Social Media']
    
    # Create sales reps
    sales_reps = list(range(1, 51))  # 50 sales reps
    
    rows = []
    
    for i in range(1, n+1):
        # Select random account and one of its contacts
        account = random.choice(accounts)
        account_contacts = [c for c in contacts if c['account_id'] == account['account_id']]
        contact = random.choice(account_contacts) if account_contacts else None
        
        created = fake.date_between(start_date='-3y', end_date='today')
        last_modified = fake.date_between(start_date=created, end_date='today')
        
        # Weight stages - more early stage opportunities
        stage = random.choices(stages, weights=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03])[0]
        
        # Close date logic
        if stage in ['Closed Won', 'Closed Lost']:
            close_date = fake.date_between(start_date=created, end_date='today').strftime('%Y-%m-%d')
        else:
            close_date = fake.date_between(start_date='today', end_date='+6m').strftime('%Y-%m-%d')
        
        # Amount varies by stage and account size
        base_amount = random.randint(5000, 500000)
        if 'Enterprise' in account.get('company_size', ''):
            base_amount *= random.uniform(2, 5)
        
        rows.append({
            'opportunity_id': i,
            'account_id': account['account_id'],
            'contact_id': contact['contact_id'] if contact else '',
            'opportunity_name': f"{account['account_name']} - {fake.catch_phrase()}",
            'stage': stage,
            'amount': round(base_amount, 2),
            'probability': stage_probabilities[stage],
            'close_date': close_date,
            'created_date': created.strftime('%Y-%m-%d'),
            'last_modified_date': last_modified.strftime('%Y-%m-%d'),
            'sales_rep_id': random.choice(sales_reps),
            'lead_source': random.choice(lead_sources)
        })
    
    write_csv('core', 'opportunities', fieldnames, rows)
    return rows

# 5. SALES PIPELINE METRICS TABLE
def generate_sales_pipeline_metrics():
    fieldnames = [
        'pipeline_id', 'date', 'stage', 'conversion_rate', 'average_deal_size', 
        'deal_velocity_days', 'win_rate', 'loss_rate', 'pipeline_value'
    ]
    
    stages = ['Prospecting', 'Qualification', 'Proposal', 'Negotiation', 'Closed Won', 'Closed Lost']
    
    rows = []
    pipeline_id = 1
    
    # Generate daily metrics for 3 years
    start_date = datetime.now().date() - timedelta(days=3*365)
    end_date = datetime.now().date()
    
    for current_date in date_range(start_date, end_date):
        for stage in stages:
            # Base conversion rates by stage
            base_conversion = {'Prospecting': 0.15, 'Qualification': 0.35, 'Proposal': 0.65, 
                             'Negotiation': 0.80, 'Closed Won': 1.0, 'Closed Lost': 0.0}
            
            conversion_rate = base_conversion[stage] + random.uniform(-0.05, 0.05)
            conversion_rate = max(0, min(1, conversion_rate))  # Keep between 0 and 1
            
            rows.append({
                'pipeline_id': pipeline_id,
                'date': current_date.strftime('%Y-%m-%d'),
                'stage': stage,
                'conversion_rate': round(conversion_rate, 3),
                'average_deal_size': round(random.uniform(25000, 150000), 2),
                'deal_velocity_days': random.randint(30, 180),
                'win_rate': round(random.uniform(0.15, 0.35), 3),
                'loss_rate': round(random.uniform(0.10, 0.25), 3),
                'pipeline_value': round(random.uniform(500000, 5000000), 2)
            })
            pipeline_id += 1
    
    write_csv('core', 'sales_pipeline_metrics', fieldnames, rows)
    return rows

# 6. CUSTOMER LIFECYCLE DATA TABLE
def generate_customer_lifecycle_data(accounts):
    fieldnames = [
        'customer_id', 'account_id', 'lifecycle_stage', 'acquisition_date', 
        'first_purchase_date', 'ltv', 'acquisition_cost', 'segment', 'risk_score'
    ]
    
    lifecycle_stages = ['Lead', 'MQL', 'SQL', 'Opportunity', 'Customer', 'Advocate', 'Churned']
    segments = ['SMB', 'Mid-Market', 'Enterprise', 'Strategic']
    
    rows = []
    customer_id = 1
    
    # Only create lifecycle data for Customer accounts
    customer_accounts = [acc for acc in accounts if acc['account_type'] == 'Customer']
    
    for account in customer_accounts:
        acquisition_date = fake.date_between(
            start_date=datetime.strptime(account['created_date'], '%Y-%m-%d').date(),
            end_date='today'
        )
        
        first_purchase = fake.date_between(start_date=acquisition_date, end_date='today')
        
        # Segment based on annual revenue
        annual_rev = account['annual_revenue']
        if annual_rev < 1_000_000:
            segment = 'SMB'
        elif annual_rev < 10_000_000:
            segment = 'Mid-Market'
        elif annual_rev < 100_000_000:
            segment = 'Enterprise'
        else:
            segment = 'Strategic'
        
        rows.append({
            'customer_id': customer_id,
            'account_id': account['account_id'],
            'lifecycle_stage': random.choices(lifecycle_stages, weights=[0.05, 0.1, 0.1, 0.15, 0.5, 0.08, 0.02])[0],
            'acquisition_date': acquisition_date.strftime('%Y-%m-%d'),
            'first_purchase_date': first_purchase.strftime('%Y-%m-%d'),
            'ltv': round(random.uniform(10000, 500000), 2),
            'acquisition_cost': round(random.uniform(1000, 25000), 2),
            'segment': segment,
            'risk_score': round(random.uniform(0, 100), 1)
        })
        customer_id += 1
    
    write_csv('core', 'customer_lifecycle_data', fieldnames, rows)
    return rows

# 7. REVENUE RECOGNITION DATA TABLE
def generate_revenue_recognition_data(opportunities):
    fieldnames = [
        'booking_id', 'opportunity_id', 'booking_date', 'booking_amount', 
        'billing_date', 'billing_amount', 'collection_date', 'collection_amount', 'revenue_type'
    ]
    
    revenue_types = ['New Business', 'Expansion', 'Renewal', 'Professional Services']
    
    rows = []
    booking_id = 1
    
    # Only create revenue data for Closed Won opportunities
    closed_won_opps = [opp for opp in opportunities if opp['stage'] == 'Closed Won']
    
    for opp in closed_won_opps:
        # Each opportunity might have multiple bookings (e.g., multi-year deals)
        num_bookings = random.choices([1, 2, 3], weights=[0.7, 0.25, 0.05])[0]
        
        for i in range(num_bookings):
            booking_date = datetime.strptime(opp['close_date'], '%Y-%m-%d').date()
            
            # Billing typically happens same day or within 30 days
            billing_date = booking_date + timedelta(days=random.randint(0, 30))
            
            # Collection typically happens 30-60 days after billing
            collection_date = billing_date + timedelta(days=random.randint(30, 60))
            
            # Amount might be split across bookings
            booking_amount = float(opp['amount']) / num_bookings
            billing_amount = booking_amount * random.uniform(0.95, 1.0)  # Slight variation
            collection_amount = billing_amount * random.uniform(0.98, 1.0)  # Account for discounts
            
            rows.append({
                'booking_id': booking_id,
                'opportunity_id': opp['opportunity_id'],
                'booking_date': booking_date.strftime('%Y-%m-%d'),
                'booking_amount': round(booking_amount, 2),
                'billing_date': billing_date.strftime('%Y-%m-%d'),
                'billing_amount': round(billing_amount, 2),
                'collection_date': collection_date.strftime('%Y-%m-%d'),
                'collection_amount': round(collection_amount, 2),
                'revenue_type': random.choice(revenue_types)
            })
            booking_id += 1
    
    write_csv('core', 'revenue_recognition_data', fieldnames, rows)
    return rows

# MAIN EXECUTION FOR CORE REVENUE DATA
def generate_core_revenue_data():
    print("Generating Core Revenue Data...")
    print("=" * 50)
    
    # Generate in dependency order
    accounts = generate_accounts(5000)
    contacts = generate_contacts(accounts)
    leads = generate_leads(75000)
    opportunities = generate_opportunities(accounts, contacts, 15000)
    sales_pipeline_metrics = generate_sales_pipeline_metrics()
    customer_lifecycle_data = generate_customer_lifecycle_data(accounts)
    revenue_recognition_data = generate_revenue_recognition_data(opportunities)
    
    print("=" * 50)
    print("Core Revenue Data generation complete!")
    print(f"Output directory: {output_dir}")

# Execute the generation
generate_core_revenue_data()