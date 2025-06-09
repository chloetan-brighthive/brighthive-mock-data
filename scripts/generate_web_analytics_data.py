import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from faker import Faker
import uuid

# Set random seed for reproducibility
np.random.seed(42)
fake = Faker()

# Create output directory with current date
output_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'output',
    f'web_analytics_{datetime.now().strftime("%m-%d")}'
)
os.makedirs(output_dir, exist_ok=True)

def generate_visitors(n_visitors, start_date, end_date):
    """Generate visitors dataset"""
    professions = [
        'Real Estate',
        'Healthcare',
        'Financial Services',
        'Teacher Education',
        'Valuation Services',
        'Accounting',
        'Other'
    ]
    profession_weights = [
        0.20,  # Real Estate
        0.20,  # Healthcare
        0.20,  # Financial Services
        0.15,  # Teacher Education
        0.10,  # Valuation Services
        0.10,  # Accounting
        0.05   # Other
    ]
    education_levels = ['High School', 'Bachelor', 'Master', 'PhD', 'Other']

    visitors = {
        'visitor_id': [str(uuid.uuid4()) for _ in range(n_visitors)],
        'user_id': [str(uuid.uuid4()) if np.random.random() < 0.3 else None for _ in range(n_visitors)],
        'first_visit_date': [
            fake.date_time_between(start_date=start_date, end_date=end_date)
            for _ in range(n_visitors)
        ],
        'profession': np.random.choice(professions, n_visitors, p=profession_weights),
        'education_level': np.random.choice(education_levels, n_visitors),
        'country': [fake.country() for _ in range(n_visitors)],
        'state_region': [fake.state() for _ in range(n_visitors)],
        'city': [fake.city() for _ in range(n_visitors)],
        'device_type': np.random.choice(['mobile', 'desktop', 'tablet'], n_visitors, p=[0.5, 0.4, 0.1])
    }

    return pd.DataFrame(visitors)

def generate_campaigns(start_date, end_date):
    """Generate campaigns dataset"""
    campaign_types = ['Email', 'Social', 'Search', 'Display', 'Affiliate']
    n_campaigns = 48  # 2 campaigns per month for 2 years

    campaigns = {
        'campaign_id': [str(uuid.uuid4()) for _ in range(n_campaigns)],
        'campaign_name': [f"Campaign_{i+1}" for i in range(n_campaigns)],
        'channel': np.random.choice(campaign_types, n_campaigns),
        'start_date': [
            fake.date_time_between(start_date=start_date, end_date=end_date - timedelta(days=30))
            for _ in range(n_campaigns)
        ],
        'end_date': [
            fake.date_time_between(start_date=start_date + timedelta(days=30), end_date=end_date)
            for _ in range(n_campaigns)
        ],
        'budget': np.random.uniform(500, 5000, n_campaigns)
    }

    return pd.DataFrame(campaigns)

def generate_pages():
    """Generate pages dataset"""
    page_types = ['product', 'landing', 'checkout', 'blog', 'category']
    n_pages = 200  # Smaller content footprint

    pages = {
        'page_url': [f"/page_{i}" for i in range(n_pages)],
        'page_title': [f"Page Title {i}" for i in range(n_pages)],
        'page_type': np.random.choice(page_types, n_pages)
    }

    return pd.DataFrame(pages)

def generate_visits(visitors_df, campaigns_df, n_visits, start_date, end_date):
    """Generate visits dataset"""
    channels = ['organic_search', 'paid_search', 'social', 'direct', 'referral']

    visits = {
        'visit_id': [str(uuid.uuid4()) for _ in range(n_visits)],
        'visitor_id': np.random.choice(visitors_df['visitor_id'], n_visits),
        'session_start_time': [
            fake.date_time_between(start_date=start_date, end_date=end_date)
            for _ in range(n_visits)
        ],
        'duration_in_seconds': np.random.exponential(300, n_visits),
        'is_bounce': np.random.choice([True, False], n_visits, p=[0.3, 0.7]),
        'channel': np.random.choice(channels, n_visits),
        'campaign_id': [
            np.random.choice(campaigns_df['campaign_id']) if np.random.random() < 0.3
            else None for _ in range(n_visits)
        ],
        'estimated_revenue': np.random.exponential(50, n_visits),
        'nb_pageviews': np.random.poisson(3, n_visits) + 1
    }

    visits_df = pd.DataFrame(visits)
    visits_df['session_end_time'] = visits_df.apply(
        lambda x: x['session_start_time'] + timedelta(seconds=x['duration_in_seconds']),
        axis=1
    )
    return visits_df

def generate_orders(visits_df):
    """Generate orders dataset"""
    # Filter visits with conversion (assume 2% conversion rate)
    converting_visits = visits_df.sample(frac=0.02, random_state=42)

    orders = {
        'order_id': [str(uuid.uuid4()) for _ in range(len(converting_visits))],
        'visit_id': converting_visits['visit_id'],
        'visitor_id': converting_visits['visitor_id'],
        'order_datetime': converting_visits['session_start_time'],
        'order_value': np.random.exponential(100, len(converting_visits)),
        'items_count': np.random.poisson(2, len(converting_visits)) + 1
    }

    return pd.DataFrame(orders)

def generate_pageviews(visits_df, pages_df):
    """Generate pageviews dataset"""
    pageviews = []

    for _, visit in visits_df.iterrows():
        n_pages = int(visit['nb_pageviews'])
        pages = np.random.choice(pages_df['page_url'], n_pages)

        for i, page in enumerate(pages):
            pageviews.append({
                'pageview_id': str(uuid.uuid4()),
                'visit_id': visit['visit_id'],
                'visitor_id': visit['visitor_id'],
                'page_url': page,
                'timestamp': visit['session_start_time'] + timedelta(seconds=i*30),
                'is_entry': i == 0,
                'is_exit': i == (n_pages - 1)
            })

    return pd.DataFrame(pageviews)

def generate_form_events(visits_df):
    """Generate form events dataset"""
    # Select 10% of visits for form interactions
    form_visits = visits_df.sample(frac=0.1, random_state=42)
    event_types = ['view', 'start', 'submit', 'resubmit']

    form_events = []
    for _, visit in form_visits.iterrows():
        n_events = np.random.randint(1, 4)
        for _ in range(n_events):
            duration = max(1, int(visit['duration_in_seconds']))
            form_events.append({
                'form_event_id': str(uuid.uuid4()),
                'visit_id': visit['visit_id'],
                'form_id': f"form_{np.random.randint(1, 6)}",
                'event_type': np.random.choice(event_types),
                'timestamp': visit['session_start_time'] + timedelta(seconds=np.random.randint(0, duration)),
                'time_spent': np.random.exponential(30)
            })

    return pd.DataFrame(form_events)

def generate_media_events(visits_df):
    """Generate media events dataset"""
    # Select 5% of visits for media interactions
    media_visits = visits_df.sample(frac=0.05, random_state=42)
    event_types = ['play', 'impression', 'finish']
    media_types = ['video', 'audio']

    media_events = []
    for _, visit in media_visits.iterrows():
        n_events = np.random.randint(1, 3)
        for _ in range(n_events):
            duration = max(1, int(visit['duration_in_seconds']))
            media_events.append({
                'media_event_id': str(uuid.uuid4()),
                'visit_id': visit['visit_id'],
                'media_type': np.random.choice(media_types),
                'event_type': np.random.choice(event_types),
                'timestamp': visit['session_start_time'] + timedelta(seconds=np.random.randint(0, duration)),
                'duration_watched': np.random.exponential(60)
            })

    return pd.DataFrame(media_events)

def main():
    print("Generating datasets...")

    # Set date range for 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)  # 2 years

    # Data size parameters
    n_visitors = 110000
    n_visits = 180000

    # Generate base datasets
    visitors_df = generate_visitors(n_visitors, start_date, end_date)
    campaigns_df = generate_campaigns(start_date, end_date)
    pages_df = generate_pages()
    visits_df = generate_visits(visitors_df, campaigns_df, n_visits, start_date, end_date)
    orders_df = generate_orders(visits_df)
    pageviews_df = generate_pageviews(visits_df, pages_df)
    form_events_df = generate_form_events(visits_df)
    media_events_df = generate_media_events(visits_df)

    # Save datasets
    print(f"Saving datasets to {output_dir}")

    datasets = {
        'visitors': visitors_df,
        'campaigns': campaigns_df,
        'pages': pages_df,
        'visits': visits_df,
        'orders': orders_df,
        'pageviews': pageviews_df,
        'form_events': form_events_df,
        'media_events': media_events_df
    }

    for name, df in datasets.items():
        # Save as CSV
        df.to_csv(os.path.join(output_dir, f'web_analytics__{name}_{datetime.now().strftime("%m-%d")}.csv'), index=False)

    print("Data generation complete!")

if __name__ == "__main__":
    main()