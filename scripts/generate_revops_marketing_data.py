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

# Output directory (assuming core data was already generated)
today_str = datetime.now().strftime("%m-%d")
script_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else '.'
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

# 1. MARKETING ATTRIBUTION DATA
def generate_marketing_attribution_data(n=45000):
    fieldnames = [
        'attribution_id', 'campaign_id', 'campaign_name', 'channel', 'lead_id', 
        'opportunity_id', 'attribution_model', 'credit_percentage', 'spend', 'revenue_attributed'
    ]
    
    channels = ['Paid Search', 'Social Media', 'Email', 'Content Marketing', 'Webinar', 
               'Trade Show', 'Partner', 'Direct', 'Organic Search', 'Display Ads']
    attribution_models = ['First Touch', 'Last Touch', 'Linear', 'Time Decay', 'Position Based']
    
    # Generate campaign data first
    campaigns = []
    for i in range(1, 201):  # 200 campaigns over 3 years
        campaigns.append({
            'campaign_id': i,
            'campaign_name': f"{random.choice(['Q1', 'Q2', 'Q3', 'Q4'])} {random.choice(['2022', '2023', '2024'])} {fake.catch_phrase()}",
            'channel': random.choice(channels),
            'spend': round(random.uniform(5000, 100000), 2)
        })
    
    rows = []
    for i in range(1, n+1):
        campaign = random.choice(campaigns)
        
        # Attribution credit varies by model
        model = random.choice(attribution_models)
        if model == 'Linear':
            credit = round(random.uniform(0.1, 0.5), 3)
        elif model in ['First Touch', 'Last Touch']:
            credit = 1.0
        else:
            credit = round(random.uniform(0.2, 0.8), 3)
        
        # Revenue attributed based on spend and performance
        revenue_multiplier = random.uniform(0.5, 8.0)  # ROI varies widely
        revenue_attributed = campaign['spend'] * revenue_multiplier * credit
        
        rows.append({
            'attribution_id': i,
            'campaign_id': campaign['campaign_id'],
            'campaign_name': campaign['campaign_name'],
            'channel': campaign['channel'],
            'lead_id': random.randint(1, 75000),  # Reference to leads from core data
            'opportunity_id': random.randint(1, 15000) if random.random() < 0.3 else '',  # 30% have opportunities
            'attribution_model': model,
            'credit_percentage': credit,
            'spend': round(campaign['spend'] * credit, 2),
            'revenue_attributed': round(revenue_attributed, 2)
        })
    
    write_csv('marketing', 'marketing_attribution', fieldnames, rows)
    return rows

# 2. WEBSITE ANALYTICS DATA
def generate_website_analytics_data(n=1095000):  # ~1000 sessions per day for 3 years
    fieldnames = [
        'session_id', 'date', 'user_id', 'page_views', 'session_duration', 
        'bounce_rate', 'conversion_event', 'traffic_source', 'device_type', 'geography'
    ]
    
    traffic_sources = ['Organic Search', 'Paid Search', 'Social Media', 'Email', 'Direct', 
                      'Referral', 'Display Ads', 'Video Ads']
    device_types = ['Desktop', 'Mobile', 'Tablet']
    conversion_events = ['', 'Form Submit', 'Download', 'Demo Request', 'Trial Signup', 'Contact Us']
    countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Australia', 'Japan']
    
    rows = []
    
    # Generate data in chunks to avoid memory issues
    start_date = datetime.now().date() - timedelta(days=3*365)
    end_date = datetime.now().date()
    
    session_id = 1
    user_id = 1
    
    for current_date in date_range(start_date, end_date):
        # Sessions per day varies (weekends lower, some seasonal patterns)
        if current_date.weekday() >= 5:  # Weekend
            daily_sessions = random.randint(600, 800)
        else:  # Weekday
            daily_sessions = random.randint(900, 1200)
        
        for _ in range(daily_sessions):
            # Session duration in seconds
            duration = random.randint(30, 1800)  # 30 seconds to 30 minutes
            
            # Bounce rate calculation
            if duration < 60:
                bounce = 1
            else:
                bounce = 0
            
            # Page views correlated with duration
            if duration < 120:
                page_views = 1
            elif duration < 300:
                page_views = random.randint(2, 4)
            else:
                page_views = random.randint(3, 15)
            
            # Conversion events are rare
            conversion = random.choices(conversion_events, weights=[0.85, 0.05, 0.04, 0.03, 0.02, 0.01])[0]
            
            rows.append({
                'session_id': str(uuid.uuid4()),
                'date': current_date.strftime('%Y-%m-%d'),
                'user_id': f"user_{user_id}",
                'page_views': page_views,
                'session_duration': duration,
                'bounce_rate': bounce,
                'conversion_event': conversion,
                'traffic_source': random.choice(traffic_sources),
                'device_type': random.choices(device_types, weights=[0.5, 0.4, 0.1])[0],
                'geography': random.choice(countries)
            })
            
            session_id += 1
            if random.random() < 0.3:  # 30% chance of new user
                user_id += 1
    
    # Write in chunks to avoid memory issues
    chunk_size = 50000
    for i in range(0, len(rows), chunk_size):
        chunk = rows[i:i+chunk_size]
        if i == 0:
            write_csv('marketing', 'website_analytics', fieldnames, chunk)
        else:
            # Append to existing file
            filename = f"{output_dir}/revops_marketing_website_analytics.csv"
            with open(filename, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                for row in chunk:
                    writer.writerow(row)
    
    print(f"Total website analytics records: {len(rows)}")
    return rows[:1000]  # Return sample for memory

# 3. LEAD SCORING DATA
def generate_lead_scoring_data(n=225000):  # ~3 scores per lead on average
    fieldnames = [
        'lead_id', 'email_engagement_score', 'website_activity_score', 
        'demographic_score', 'firmographic_score', 'total_score', 'score_date'
    ]
    
    rows = []
    score_id = 1
    
    # Generate multiple scores per lead over time
    for lead_id in range(1, 75001):  # For each lead
        num_scores = random.choices([1, 2, 3, 4, 5], weights=[0.3, 0.25, 0.25, 0.15, 0.05])[0]
        
        base_date = fake.date_between(start_date='-3y', end_date='today')
        
        for i in range(num_scores):
            # Scores evolve over time
            score_date = base_date + timedelta(days=random.randint(0, 365))
            
            # Individual component scores (0-100)
            email_score = random.randint(0, 100)
            website_score = random.randint(0, 100)
            demo_score = random.randint(0, 100)
            firmo_score = random.randint(0, 100)
            
            # Total score is weighted average
            total_score = round((email_score * 0.3 + website_score * 0.3 + 
                              demo_score * 0.2 + firmo_score * 0.2), 1)
            
            rows.append({
                'lead_id': lead_id,
                'email_engagement_score': email_score,
                'website_activity_score': website_score,
                'demographic_score': demo_score,
                'firmographic_score': firmo_score,
                'total_score': total_score,
                'score_date': score_date.strftime('%Y-%m-%d')
            })
            
            # Scores generally improve over time
            base_date = score_date
    
    write_csv('marketing', 'lead_scoring', fieldnames, rows)
    return rows

# 4. MARKETING AUTOMATION DATA
def generate_marketing_automation_data(n=180000):
    fieldnames = [
        'campaign_id', 'email_id', 'contact_id', 'sent_date', 'open_rate', 
        'click_rate', 'conversion_rate', 'unsubscribe_rate', 'campaign_type'
    ]
    
    campaign_types = ['Newsletter', 'Product Update', 'Nurture Sequence', 'Event Invitation', 
                     'Webinar', 'Case Study', 'Trial Reminder', 'Onboarding']
    
    rows = []
    
    # Generate campaigns first
    campaigns = []
    for i in range(1, 501):  # 500 email campaigns over 3 years
        campaigns.append({
            'campaign_id': i,
            'campaign_type': random.choice(campaign_types),
            'base_open_rate': random.uniform(0.15, 0.35),
            'base_click_rate': random.uniform(0.02, 0.08),
            'base_conversion_rate': random.uniform(0.005, 0.03),
            'base_unsubscribe_rate': random.uniform(0.001, 0.01)
        })
    
    email_id = 1
    
    for campaign in campaigns:
        # Each campaign has multiple emails sent to different contacts
        emails_in_campaign = random.randint(100, 2000)
        
        for _ in range(emails_in_campaign):
            sent_date = fake.date_between(start_date='-3y', end_date='today')
            
            # Performance varies around base rates
            open_rate = max(0, min(1, campaign['base_open_rate'] + random.uniform(-0.05, 0.05)))
            click_rate = max(0, min(open_rate, campaign['base_click_rate'] + random.uniform(-0.02, 0.02)))
            conversion_rate = max(0, min(click_rate, campaign['base_conversion_rate'] + random.uniform(-0.01, 0.01)))
            unsubscribe_rate = max(0, min(0.05, campaign['base_unsubscribe_rate'] + random.uniform(-0.002, 0.002)))
            
            rows.append({
                'campaign_id': campaign['campaign_id'],
                'email_id': email_id,
                'contact_id': random.randint(1, 25000),  # Reference to contacts from core data
                'sent_date': sent_date.strftime('%Y-%m-%d'),
                'open_rate': round(open_rate, 4),
                'click_rate': round(click_rate, 4),
                'conversion_rate': round(conversion_rate, 4),
                'unsubscribe_rate': round(unsubscribe_rate, 4),
                'campaign_type': campaign['campaign_type']
            })
            
            email_id += 1
            
            if len(rows) >= n:
                break
        
        if len(rows) >= n:
            break
    
    write_csv('marketing', 'marketing_automation', fieldnames, rows)
    return rows

# MAIN EXECUTION FOR MARKETING DATA
def generate_marketing_data():
    print("Generating Marketing & Lead Generation Data...")
    print("=" * 60)
    
    # Generate all marketing tables
    marketing_attribution = generate_marketing_attribution_data(45000)
    website_analytics = generate_website_analytics_data(1095000)  # This will be large
    lead_scoring = generate_lead_scoring_data(225000)
    marketing_automation = generate_marketing_automation_data(180000)
    
    print("=" * 60)
    print("Marketing & Lead Generation data generation complete!")
    print(f"Output directory: {output_dir}")

# Execute the generation
generate_marketing_data()