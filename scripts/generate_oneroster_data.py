import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
from faker import Faker
import uuid

np.random.seed(42)
fake = Faker()

# Output directory
output_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'output',
    f'oneroster_{datetime.now().strftime("%m-%d")}'
)
os.makedirs(output_dir, exist_ok=True)

# Row counts
N_SESSIONS = 8
N_ORGS = 60
N_USERS = 15000
N_CLASSES = 1500
N_COURSES = 300
N_ENROLLMENTS = 40000
N_GRADING_PERIODS = 16
N_LINEITEMS = 7000
N_RESULTS = 80000
N_CATEGORIES = 7

def generate_academic_sessions(n):
    sessions = []
    base_year = datetime.now().year - 3
    for i in range(n):
        year = base_year + i // 2
        term = 'Fall' if i % 2 == 0 else 'Spring'
        start = datetime(year, 8, 15) if term == 'Fall' else datetime(year + 1, 1, 10)
        end = datetime(year, 12, 20) if term == 'Fall' else datetime(year + 1, 5, 25)
        sessions.append({
            'sourcedId': str(uuid.uuid4()),
            'title': f'{term} {year}',
            'startDate': start.date(),
            'endDate': end.date(),
            'type': 'term',
            'parent': ''
        })
    return pd.DataFrame(sessions)

def generate_organizations(n):
    orgs = []
    district_id = str(uuid.uuid4())
    orgs.append({
        'sourcedId': district_id,
        'name': fake.company() + " District",
        'type': 'district',
        'identifier': fake.bothify(text='DIST-####'),
        'parent': ''
    })
    for i in range(n - 1):
        orgs.append({
            'sourcedId': str(uuid.uuid4()),
            'name': fake.company() + " School",
            'type': 'school',
            'identifier': fake.bothify(text='SCH-####'),
            'parent': district_id
        })
    return pd.DataFrame(orgs)

def generate_users(n, org_ids):
    roles = ['student'] * 8 + ['teacher'] * 1 + ['admin']
    users = []
    for _ in range(n):
        role = np.random.choice(roles)
        org = np.random.choice(org_ids)
        users.append({
            'sourcedId': str(uuid.uuid4()),
            'username': fake.user_name(),
            'givenName': fake.first_name(),
            'familyName': fake.last_name(),
            'role': role,
            'orgSourcedIds': org,
            'userIds': fake.bothify(text='U-#####'),
            'email': fake.email()
        })
    return pd.DataFrame(users)

def generate_courses(n, org_ids):
    courses = []
    for _ in range(n):
        courses.append({
            'sourcedId': str(uuid.uuid4()),
            'title': fake.catch_phrase(),
            'courseCode': fake.bothify(text='C-####'),
            'orgSourcedId': np.random.choice(org_ids)
        })
    return pd.DataFrame(courses)

def generate_classes(n, course_ids, org_ids, session_ids):
    subjects = ['Math', 'Science', 'English', 'History', 'Art', 'Music', 'PE', 'Technology']
    classes = []
    for _ in range(n):
        course = np.random.choice(course_ids)
        school = np.random.choice(org_ids)
        term = np.random.choice(session_ids)
        classes.append({
            'sourcedId': str(uuid.uuid4()),
            'title': fake.bs().title(),
            'courseSourcedId': course,
            'schoolSourcedId': school,
            'termSourcedIds': term,
            'subjects': np.random.choice(subjects),
            'classCode': fake.bothify(text='CL-####')
        })
    return pd.DataFrame(classes)

def generate_enrollments(n, user_ids, class_ids):
    roles = ['student'] * 8 + ['teacher'] * 2
    statuses = ['active', 'inactive']
    enrollments = []
    for _ in range(n):
        enrollments.append({
            'sourcedId': str(uuid.uuid4()),
            'userSourcedId': np.random.choice(user_ids),
            'classSourcedId': np.random.choice(class_ids),
            'role': np.random.choice(roles),
            'status': np.random.choice(statuses, p=[0.95, 0.05]),
            'beginDate': fake.date_between(start_date='-3y', end_date='today'),
            'endDate': fake.date_between(start_date='today', end_date='+1y')
        })
    return pd.DataFrame(enrollments)

def generate_grading_periods(n, session_ids):
    periods = []
    for i in range(n):
        session = np.random.choice(session_ids)
        periods.append({
            'sourcedId': str(uuid.uuid4()),
            'title': f'Grading Period {i+1}',
            'startDate': fake.date_between(start_date='-3y', end_date='today'),
            'endDate': fake.date_between(start_date='today', end_date='+1y'),
            'sessionSourcedId': session
        })
    return pd.DataFrame(periods)

def generate_categories(n):
    titles = ['Homework', 'Quiz', 'Exam', 'Project', 'Participation', 'Lab', 'Other']
    weights = np.random.dirichlet(np.ones(n), size=1)[0]
    categories = []
    for i in range(n):
        categories.append({
            'sourcedId': str(uuid.uuid4()),
            'title': titles[i % len(titles)],
            'weight': round(weights[i], 2)
        })
    return pd.DataFrame(categories)

def generate_lineitems(n, class_ids, category_ids, grading_period_ids):
    lineitems = []
    for _ in range(n):
        lineitems.append({
            'sourcedId': str(uuid.uuid4()),
            'title': fake.sentence(nb_words=3),
            'classSourcedId': np.random.choice(class_ids),
            'category': np.random.choice(category_ids),
            'gradingPeriodSourcedId': np.random.choice(grading_period_ids)
        })
    return pd.DataFrame(lineitems)

def generate_results(n, lineitem_ids, student_ids):
    statuses = ['submitted', 'graded', 'missing']
    results = []
    for _ in range(n):
        results.append({
            'sourcedId': str(uuid.uuid4()),
            'lineItemSourcedId': np.random.choice(lineitem_ids),
            'studentSourcedId': np.random.choice(student_ids),
            'score': round(np.random.uniform(0, 100), 2),
            'status': np.random.choice(statuses, p=[0.7, 0.25, 0.05])
        })
    return pd.DataFrame(results)

def main():
    print("Generating OneRoster datasets...")

    # Generate base tables
    academic_sessions_df = generate_academic_sessions(N_SESSIONS)
    organizations_df = generate_organizations(N_ORGS)
    users_df = generate_users(N_USERS, organizations_df['sourcedId'].tolist())
    courses_df = generate_courses(N_COURSES, organizations_df['sourcedId'].tolist())
    classes_df = generate_classes(N_CLASSES, courses_df['sourcedId'].tolist(), organizations_df['sourcedId'].tolist(), academic_sessions_df['sourcedId'].tolist())
    enrollments_df = generate_enrollments(N_ENROLLMENTS, users_df['sourcedId'].tolist(), classes_df['sourcedId'].tolist())
    grading_periods_df = generate_grading_periods(N_GRADING_PERIODS, academic_sessions_df['sourcedId'].tolist())
    categories_df = generate_categories(N_CATEGORIES)
    lineitems_df = generate_lineitems(N_LINEITEMS, classes_df['sourcedId'].tolist(), categories_df['sourcedId'].tolist(), grading_periods_df['sourcedId'].tolist())
    # Only students get results
    student_ids = users_df[users_df['role'] == 'student']['sourcedId'].tolist()
    results_df = generate_results(N_RESULTS, lineitems_df['sourcedId'].tolist(), student_ids)

    # Save all tables
    datasets = {
        'academic_sessions': academic_sessions_df,
        'organizations': organizations_df,
        'users': users_df,
        'classes': classes_df,
        'courses': courses_df,
        'enrollments': enrollments_df,
        'grading_periods': grading_periods_df,
        'lineitems': lineitems_df,
        'results': results_df,
        'categories': categories_df
    }

    for name, df in datasets.items():
        filename = f'oneroster__{name}_{datetime.now().strftime("%m-%d")}.csv'
        df.to_csv(os.path.join(output_dir, filename), index=False)

    print(f"Data generation complete! Files saved to {output_dir}")

if __name__ == "__main__":
    main()