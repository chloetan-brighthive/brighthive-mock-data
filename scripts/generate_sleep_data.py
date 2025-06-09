import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import uuid

def create_sleep_dataset(num_users=25, days_per_user=30):
    """
    Generate sleep dataset for multiple users over specified number of days
    
    Args:
        num_users: Number of unique users to generate
        days_per_user: Number of days of sleep data per user
    """
    # Get current date for file naming
    current_date = datetime.now().strftime("%m-%d")

    # Generate user IDs
    user_ids = [f"USER_{str(uuid.uuid4())[:8]}" for _ in range(num_users)]

    # Create user profiles with consistent baseline metrics
    user_profiles = {
        user_id: {
            'base_hr': np.random.randint(55, 75),
            'base_hrv': np.random.randint(30, 50),
            'base_breath': round(np.random.uniform(12, 18), 1),
            'typical_bedtime': datetime.strptime(
                f"{np.random.randint(21, 24):02d}:{np.random.randint(0, 60):02d}",
                "%H:%M"
            ).time(),
            'sleep_duration_preference': np.random.randint(360, 540)  # in minutes
        } for user_id in user_ids
    }

    # Define possible values for categorical fields
    sleep_types = ['long_sleep', 'short_sleep', 'nap']
    algorithm_versions = ['v1', 'v2', 'v2.1']

    # Define ranges for numerical values
    hr_ranges = {
        'average': (55, 75),
        'lowest': (45, 55),
        'hrv': (30, 50),
        'breath': (12, 18)
    }

    sleep_duration_ranges = {
        'total': (360, 540),  # 6-9 hours in minutes
        'deep_pct': (0.15, 0.25),
        'rem_pct': (0.20, 0.30),
        'light_pct': (0.40, 0.50)
    }

    readiness_contributors = [
        'activity_balance',
        'body_temperature',
        'hrv_balance',
        'previous_day_activity',
        'previous_night',
        'recovery_index',
        'resting_heart_rate',
        'sleep_balance'
    ]

    def generate_time_series(start_time, duration_minutes, interval_seconds=300):
        """Generate time series data with specified interval"""
        num_points = int((duration_minutes * 60) / interval_seconds)
        timestamps = [start_time + timedelta(seconds=i*interval_seconds) for i in range(num_points)]
        return timestamps

    def generate_heart_rate_data(start_time, duration_minutes, base_hr):
        """Generate synthetic heart rate data"""
        timestamps = generate_time_series(start_time, duration_minutes)
        hr_values = [max(45, min(100, base_hr + np.random.normal(0, 5))) for _ in timestamps]
        return {
            "interval": 300,
            "items": hr_values,
            "timestamp": timestamps[0].isoformat()
        }

    def generate_hrv_data(start_time, duration_minutes, base_hrv):
        """Generate synthetic HRV data"""
        timestamps = generate_time_series(start_time, duration_minutes)
        hrv_values = [max(20, min(60, base_hrv + np.random.normal(0, 8))) for _ in timestamps]
        return {
            "interval": 300,
            "items": hrv_values,
            "timestamp": timestamps[0].isoformat()
        }

    # Generate sleep records for all users
    sleep_records = []
    
    for user_id in user_ids:
        profile = user_profiles[user_id]
        
        for day_offset in range(days_per_user):
            current_day = (datetime.now() - timedelta(days=day_offset)).date()
            
            # Generate bedtime with some variation around user's typical bedtime
            bedtime_variation = np.random.randint(-30, 30)  # ±30 minutes
            bedtime_start = datetime.combine(
                current_day,
                profile['typical_bedtime']
            ) + timedelta(minutes=bedtime_variation)

            # Generate sleep duration with variation around user's preference
            sleep_duration = profile['sleep_duration_preference'] + np.random.randint(-30, 30)
            
            # Calculate sleep stages
            deep_sleep = int(sleep_duration * np.random.uniform(
                sleep_duration_ranges['deep_pct'][0],
                sleep_duration_ranges['deep_pct'][1]
            ))
            rem_sleep = int(sleep_duration * np.random.uniform(
                sleep_duration_ranges['rem_pct'][0],
                sleep_duration_ranges['rem_pct'][1]
            ))
            light_sleep = int(sleep_duration * sleep_duration_ranges['light_pct'][0])
            awake_time = sleep_duration - (deep_sleep + rem_sleep + light_sleep)

            # Generate heart rate and HRV data based on user's baseline
            avg_hr = profile['base_hr'] + np.random.randint(-5, 5)
            avg_hrv = profile['base_hrv'] + np.random.randint(-5, 5)

            sleep_record = {
                'sleep_id': str(uuid.uuid4()),
                'user_id': user_id,
                'day': current_day.strftime("%Y-%m-%d"),
                'bedtime_start': bedtime_start.isoformat(),
                'bedtime_end': (bedtime_start + timedelta(minutes=sleep_duration)).isoformat(),
                'deep_sleep_duration': deep_sleep * 60,
                'rem_sleep_duration': rem_sleep * 60,
                'light_sleep_duration': light_sleep * 60,
                'awake_time': awake_time * 60,
                'total_sleep_duration': sleep_duration * 60,
                'average_heart_rate': avg_hr,
                'average_hrv': avg_hrv,
                'heart_rate': generate_heart_rate_data(bedtime_start, sleep_duration, avg_hr),
                'hrv': generate_hrv_data(bedtime_start, sleep_duration, avg_hrv),
                'efficiency': np.random.randint(80, 95),
                'readiness': {
                    'contributors': {
                        contributor: np.random.randint(70, 100)
                        for contributor in readiness_contributors
                    },
                    'score': np.random.randint(70, 100)
                },
                'type': np.random.choice(sleep_types),
                'sleep_algorithm_version': np.random.choice(algorithm_versions)
            }

            sleep_records.append(sleep_record)

    # Create DataFrame
    df = pd.DataFrame(sleep_records)

    # Create directory structure
    output_dir = os.path.join("output", f"sleep_data_{current_date}")
    os.makedirs(output_dir, exist_ok=True)

    # Save to CSV
    output_file = os.path.join(output_dir, f"sleep_data_{current_date}.csv")
    df.to_csv(output_file, index=False)

    # Save user profiles
    user_profiles_df = pd.DataFrame.from_dict(user_profiles, orient='index')
    user_profiles_file = os.path.join(output_dir, f"user_profiles_{current_date}.csv")
    user_profiles_df.to_csv(user_profiles_file)

    print(f"Dataset created successfully: {output_file}")
    print(f"Number of users: {num_users}")
    print(f"Total records: {len(df)}")

    return df, output_file, user_profiles_df, user_profiles_file

# Execute the function
if __name__ == "__main__":
    df, sleep_file, users_df, users_file = create_sleep_dataset(num_users=25, days_per_user=30)

    # Display sample of the dataset
    print("\nSample of sleep records:")
    print(df[['user_id', 'day', 'average_heart_rate', 'efficiency']].head())

    print("\nSample of user profiles:")
    print(users_df.head())

    # Created/Modified files during execution:
    print("\nCreated/Modified files during execution:")
    print(sleep_file)
    print(users_file)