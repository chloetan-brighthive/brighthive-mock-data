import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import uuid

def create_sleep_dataset(num_users=25, days_per_user=30):
    """
    Generate simplified sleep dataset across multiple tables
    """
    # Get current date for file naming
    current_date = datetime.now().strftime("%m-%d")

    # Create output directory
    output_dir = os.path.join("output", f"health_device_{current_date}")
    os.makedirs(output_dir, exist_ok=True)

    # Generate user IDs
    user_ids = [f"USER_{str(uuid.uuid4())[:8]}" for _ in range(num_users)]

    # 1. Generate User Profiles
    user_profiles = []
    for user_id in user_ids:
        profile = {
            'user_id': user_id,
            'base_heart_rate': int(np.random.randint(55, 75)),
            'base_hrv': int(np.random.randint(30, 50)),
            'typical_bedtime': f"{np.random.randint(21,24):02d}:{np.random.randint(0,60):02d}",
            'preferred_sleep_duration': int(np.random.randint(360, 540))  # in minutes
        }
        user_profiles.append(profile)

    user_profiles_df = pd.DataFrame(user_profiles)

    # 2. Generate Sleep Sessions
    sleep_sessions = []
    sleep_stages = []
    sleep_metrics = []
    vital_readings = []
    readiness_scores = []

    sleep_types = ['long_sleep', 'short_sleep', 'nap']
    algorithm_versions = ['v1', 'v2', 'v2.1']
    readiness_types = ['activity_balance', 'recovery_index', 'sleep_balance']

    for user_id in user_ids:
        user_profile = user_profiles_df[user_profiles_df['user_id'] == user_id].iloc[0]

        for day_offset in range(days_per_user):
            # Generate session ID
            session_id = str(uuid.uuid4())

            # Calculate times
            current_day = datetime.now() - timedelta(days=day_offset)
            typical_bedtime = datetime.strptime(user_profile['typical_bedtime'], "%H:%M").time()
            bedtime_start = datetime.combine(current_day.date(), typical_bedtime) + \
                           timedelta(minutes=int(np.random.randint(-30, 30)))
            sleep_duration = int(user_profile['preferred_sleep_duration'] + np.random.randint(-30, 30))
            bedtime_end = bedtime_start + timedelta(minutes=sleep_duration)

            # 2.1 Sleep Sessions
            sleep_sessions.append({
                'session_id': session_id,
                'user_id': user_id,
                'start_time': bedtime_start,
                'end_time': bedtime_end,
                'type': np.random.choice(sleep_types),
                'algorithm_version': np.random.choice(algorithm_versions)
            })

            # 2.2 Sleep Stages
            total_sleep = sleep_duration * 60  # convert to seconds
            sleep_stages.append({
                'session_id': session_id,
                'deep_sleep': int(total_sleep * np.random.uniform(0.15, 0.25)),
                'rem_sleep': int(total_sleep * np.random.uniform(0.20, 0.30)),
                'light_sleep': int(total_sleep * np.random.uniform(0.40, 0.50)),
                'awake': int(total_sleep * np.random.uniform(0.05, 0.10))
            })

            # 2.3 Sleep Metrics
            avg_hr = int(user_profile['base_heart_rate'] + np.random.randint(-5, 5))
            avg_hrv = int(user_profile['base_hrv'] + np.random.randint(-5, 5))
            sleep_metrics.append({
                'session_id': session_id,
                'average_heart_rate': avg_hr,
                'average_hrv': avg_hrv,
                'efficiency': int(np.random.randint(80, 95))
            })

            # 2.4 Hourly Vital Readings
            hours = int(sleep_duration / 60)
            for hour in range(hours):
                timestamp = bedtime_start + timedelta(hours=hour)
                vital_readings.append({
                    'session_id': session_id,
                    'timestamp': timestamp,
                    'heart_rate': int(avg_hr + np.random.randint(-8, 8)),
                    'hrv': int(avg_hrv + np.random.randint(-10, 10))
                })

            # 2.5 Readiness Scores
            for score_type in readiness_types:
                readiness_scores.append({
                    'session_id': session_id,
                    'score_type': score_type,
                    'value': int(np.random.randint(70, 100))
                })

    # Convert to DataFrames
    dfs = {
        'user_profiles': pd.DataFrame(user_profiles),
        'sleep_sessions': pd.DataFrame(sleep_sessions),
        'sleep_stages': pd.DataFrame(sleep_stages),
        'sleep_metrics': pd.DataFrame(sleep_metrics),
        'vital_readings': pd.DataFrame(vital_readings),
        'readiness_scores': pd.DataFrame(readiness_scores)
    }

    # Save all DataFrames to CSV
    saved_files = []
    for name, df in dfs.items():
        output_file = os.path.join(output_dir, f"health_device_{name}_{current_date}.csv")
        df.to_csv(output_file, index=False)
        saved_files.append(output_file)

    print(f"Datasets created successfully in: {output_dir}")
    print(f"Number of users: {num_users}")
    print(f"Total sleep sessions: {len(sleep_sessions)}")

    return dfs, saved_files

# Execute the function
if __name__ == "__main__":
    dfs, saved_files = create_sleep_dataset(num_users=25, days_per_user=30)

    # Display sample of each dataset
    print("\nSample of each dataset:")
    for name, df in dfs.items():
        print(f"\n{name.upper()}:")
        print(df.head(2))

    # Created/Modified files during execution:
    print("\nCreated/Modified files during execution:")
    for file in saved_files:
        print(file)