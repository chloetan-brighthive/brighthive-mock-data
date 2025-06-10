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

# 1. CUSTOMER HEALTH SCORES
def generate_customer_health_scores(n_customers=4000):
    fieldnames = [
        'health_id', 'customer_id', 'date', 'product_usage_score', 'support_score', 
        'engagement_score', 'nps_score', 'overall_health_score'
    ]
    
    rows = []
    health_id = 1
    
    # Generate monthly health scores for each customer
    start_date = datetime.now().date() - timedelta(days=3*365)
    end_date = datetime.now().date()
    
    for customer_id in range(1, n_customers + 1):
        # Customer start date (when they became a customer)
        customer_start = fake.date_between(start_date=start_date, end_date=end_date)
        
        # Generate monthly scores from customer start to present
        current_date = customer_start.replace(day=1)  # Start of month
        
        # Base scores that evolve over time
        base_usage = random.uniform(40, 90)
        base_support = random.uniform(60, 95)
        base_engagement = random.uniform(30, 85)
        base_nps = random.uniform(-50, 80)
        
        while current_date <= end_date:
            # Scores drift over time with some randomness
            usage_score = max(0, min(100, base_usage + random.uniform(-15, 15)))
            support_score = max(0, min(100, base_support + random.uniform(-10, 10)))
            engagement_score = max(0, min(100, base_engagement + random.uniform(-20, 20)))
            nps_score = max(-100, min(100, base_nps + random.uniform(-20, 20)))
            
            # Overall health is weighted average
            overall_health = round((usage_score * 0.3 + support_score * 0.2 + 
                                 engagement_score * 0.3 + (nps_score + 100) * 0.5 * 0.2), 1)
            
            rows.append({
                'health_id': health_id,
                'customer_id': customer_id,
                'date': current_date.strftime('%Y-%m-%d'),
                'product_usage_score': round(usage_score, 1),
                'support_score': round(support_score, 1),
                'engagement_score': round(engagement_score, 1),
                'nps_score': round(nps_score, 1),
                'overall_health_score': overall_health
            })
            
            health_id += 1
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                # Use timedelta to safely move to next month
                current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
            
            # Gradually evolve base scores
            base_usage += random.uniform(-2, 2)
            base_support += random.uniform(-1, 1)
            base_engagement += random.uniform(-3, 3)
            base_nps += random.uniform(-5, 5)
    
    write_csv('success', 'customer_health_scores', fieldnames, rows)
    return rows

# 2. CHURN AND RETENTION DATA
def generate_churn_and_retention_data(n_customers=4000):
    fieldnames = [
        'retention_id', 'customer_id', 'cohort_month', 'months_retained', 
        'churned', 'churn_date', 'churn_reason', 'expansion_revenue', 'renewal_rate'
    ]
    
    churn_reasons = ['Price', 'Product Fit', 'Competitor', 'Budget Cuts', 'Merger/Acquisition', 
                    'Poor Support', 'Lack of Usage', 'Feature Gap', 'Contract End']
    
    rows = []
    retention_id = 1
    
    # Generate cohort data
    start_date = datetime.now().date() - timedelta(days=3*365)
    
    for customer_id in range(1, n_customers + 1):
        # Customer acquisition date
        acquisition_date = fake.date_between(start_date=start_date, end_date='today')
        cohort_month = acquisition_date.strftime('%Y-%m')
        
        # Determine if customer churned and when
        churn_probability = random.uniform(0.05, 0.25)  # 5-25% annual churn rate
        months_active = 0
        current_date = acquisition_date
        churned = False
        churn_date = ''
        churn_reason = ''
        
        # Track customer month by month
        while current_date <= datetime.now().date() and not churned:
            months_active += 1
            
            # Check for churn each month
            monthly_churn_prob = churn_probability / 12
            if random.random() < monthly_churn_prob and months_active > 3:  # No churn in first 3 months
                churned = True
                churn_date = current_date.strftime('%Y-%m-%d')
                churn_reason = random.choice(churn_reasons)
                break
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                # Use timedelta to safely move to next month
                current_date = (current_date.replace(day=1) + timedelta(days=32)).replace(day=1)
        
        # Expansion revenue (for non-churned customers)
        expansion_revenue = 0
        if not churned and months_active > 6:
            if random.random() < 0.3:  # 30% chance of expansion
                expansion_revenue = round(random.uniform(5000, 50000), 2)
        
        # Renewal rate (for customers who had renewal opportunities)
        renewal_rate = ''
        if months_active >= 12:  # Had at least one renewal cycle
            if churned:
                renewal_rate = 0.0
            else:
                renewal_rate = round(random.uniform(0.8, 1.0), 3)
        
        rows.append({
            'retention_id': retention_id,
            'customer_id': customer_id,
            'cohort_month': cohort_month,
            'months_retained': months_active,
            'churned': 'Yes' if churned else 'No',
            'churn_date': churn_date,
            'churn_reason': churn_reason,
            'expansion_revenue': expansion_revenue,
            'renewal_rate': renewal_rate
        })
        
        retention_id += 1
    
    write_csv('success', 'churn_and_retention', fieldnames, rows)
    return rows

# 3. PRODUCT USAGE ANALYTICS
def generate_product_usage_analytics(n_customers=4000):
    fieldnames = [
        'usage_id', 'customer_id', 'date', 'feature_name', 'usage_count', 
        'session_duration', 'user_count', 'adoption_stage'
    ]
    
    features = ['Dashboard', 'Reports', 'API', 'Integrations', 'Mobile App', 
               'Advanced Analytics', 'Collaboration', 'Automation', 'Custom Fields', 'Export']
    adoption_stages = ['Trial', 'Basic', 'Intermediate', 'Advanced', 'Power User']
    
    rows = []
    usage_id = 1
    
    # Generate daily usage data (sample - not all days for all customers to keep manageable)
    start_date = datetime.now().date() - timedelta(days=365)  # Last year only
    end_date = datetime.now().date()
    
    for customer_id in range(1, n_customers + 1):
        # Customer's adoption stage
        customer_adoption = random.choice(adoption_stages)
        
        # Features used based on adoption stage
        if customer_adoption == 'Trial':
            active_features = random.sample(features, random.randint(1, 3))
        elif customer_adoption == 'Basic':
            active_features = random.sample(features, random.randint(2, 5))
        elif customer_adoption == 'Intermediate':
            active_features = random.sample(features, random.randint(4, 7))
        elif customer_adoption == 'Advanced':
            active_features = random.sample(features, random.randint(6, 9))
        else:  # Power User
            active_features = features
        
        # Generate usage data for random days (not every day)
        usage_days = random.randint(50, 300)  # 50-300 days of usage in the year
        
        for _ in range(usage_days):
            usage_date = fake.date_between(start_date=start_date, end_date=end_date)
            
            # Daily usage for each active feature
            for feature in active_features:
                if random.random() < 0.7:  # 70% chance feature is used on active day
                    
                    # Usage patterns vary by feature and adoption stage
                    base_usage = {'Trial': 2, 'Basic': 5, 'Intermediate': 12, 'Advanced': 25, 'Power User': 50}
                    usage_count = random.randint(1, base_usage[customer_adoption])
                    
                    # Session duration varies by feature
                    if feature in ['Dashboard', 'Reports']:
                        session_duration = random.randint(300, 3600)  # 5-60 minutes
                    elif feature in ['API', 'Integrations']:
                        session_duration = random.randint(60, 600)   # 1-10 minutes
                    else:
                        session_duration = random.randint(120, 1800)  # 2-30 minutes
                    
                    # User count (for multi-user accounts)
                    if customer_adoption in ['Advanced', 'Power User']:
                        user_count = random.randint(1, 10)
                    else:
                        user_count = random.randint(1, 3)
                    
                    rows.append({
                        'usage_id': usage_id,
                        'customer_id': customer_id,
                        'date': usage_date.strftime('%Y-%m-%d'),
                        'feature_name': feature,
                        'usage_count': usage_count,
                        'session_duration': session_duration,
                        'user_count': user_count,
                        'adoption_stage': customer_adoption
                    })
                    
                    usage_id += 1
    
    write_csv('success', 'product_usage_analytics', fieldnames, rows)
    return rows

# 4. SUPPORT AND SERVICE DATA
def generate_support_data(n_customers=4000):
    fieldnames = [
        'ticket_id', 'customer_id', 'created_date', 'resolved_date', 'priority', 
        'category', 'resolution_time_hours', 'satisfaction_score', 'agent_id'
    ]
    
    priorities = ['Low', 'Medium', 'High', 'Critical']
    categories = ['Technical Issue', 'Feature Request', 'Account Management', 'Billing', 
                 'Integration', 'Training', 'Bug Report', 'Performance', 'Security']
    
    rows = []
    
    # Generate support tickets over 3 years
    start_date = datetime.now().date() - timedelta(days=3*365)
    end_date = datetime.now().date()
    
    # Support agents
    agent_ids = list(range(1, 21))  # 20 support agents
    
    ticket_id = 1
    
    # Generate tickets for customers (not all customers create tickets)
    active_customers = random.sample(range(1, n_customers + 1), int(n_customers * 0.8))  # 80% create tickets
    
    for customer_id in active_customers:
        # Number of tickets per customer varies
        num_tickets = random.choices([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 
                                   weights=[0.3, 0.25, 0.2, 0.1, 0.05, 0.04, 0.03, 0.02, 0.005, 0.005])[0]
        
        for _ in range(num_tickets):
            created_date = fake.date_between(start_date=start_date, end_date=end_date)
            
            # Priority distribution
            priority = random.choices(priorities, weights=[0.4, 0.35, 0.2, 0.05])[0]
            
            # Resolution time based on priority
            if priority == 'Critical':
                resolution_hours = random.randint(1, 8)
            elif priority == 'High':
                resolution_hours = random.randint(4, 24)
            elif priority == 'Medium':
                resolution_hours = random.randint(8, 72)
            else:  # Low
                resolution_hours = random.randint(24, 168)
            
            resolved_date = created_date + timedelta(hours=resolution_hours)
            
            # Satisfaction score (1-5, higher for faster resolution)
            if resolution_hours <= 4:
                satisfaction = random.choices([3, 4, 5], weights=[0.1, 0.3, 0.6])[0]
            elif resolution_hours <= 24:
                satisfaction = random.choices([2, 3, 4, 5], weights=[0.1, 0.2, 0.4, 0.3])[0]
            else:
                satisfaction = random.choices([1, 2, 3, 4], weights=[0.2, 0.3, 0.3, 0.2])[0]
            
            rows.append({
                'ticket_id': ticket_id,
                'customer_id': customer_id,
                'created_date': created_date.strftime('%Y-%m-%d'),
                'resolved_date': resolved_date.strftime('%Y-%m-%d'),
                'priority': priority,
                'category': random.choice(categories),
                'resolution_time_hours': resolution_hours,
                'satisfaction_score': satisfaction,
                'agent_id': random.choice(agent_ids)
            })
            
            ticket_id += 1
    
    write_csv('success', 'support_data', fieldnames, rows)
    return rows

# MAIN EXECUTION FOR CUSTOMER SUCCESS DATA
def generate_customer_success_data():
    print("Generating Customer Success & Retention Data...")
    print("=" * 60)
    
    # Generate all customer success tables
    customer_health_scores = generate_customer_health_scores(4000)
    churn_and_retention = generate_churn_and_retention_data(4000)
    product_usage_analytics = generate_product_usage_analytics(4000)
    support_data = generate_support_data(4000)
    
    print("=" * 60)
    print("Customer Success & Retention data generation complete!")
    print(f"Output directory: {output_dir}")

# Execute the generation
if __name__ == "__main__":
    generate_customer_success_data()