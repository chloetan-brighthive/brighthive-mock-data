import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import string
import glob
import sys
from pathlib import Path
import logging
from typing import Dict, List, Optional

from faker import Faker

# Initialize Faker with a seed for reproducibility
fake = Faker()
Faker.seed(12345)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataValidationError(Exception):
    """Custom exception for data validation errors"""
    pass

def setup_directories() -> Path:
    """
    Dynamically finds script location and sets up directory structure.

    Returns:
        Path: Path to the new version directory

    Raises:
        OSError: If directory creation fails
    """
    try:
        # Get the script's directory
        if getattr(sys, 'frozen', False):
            script_dir = Path(sys.executable).parent
        else:
            script_dir = Path(__file__).parent.absolute()

        root_dir = script_dir.parent
        output_dir = root_dir / 'output'
        output_dir.mkdir(exist_ok=True)

        # Find existing versions
        existing_versions = list(output_dir.glob('student_v*'))
        next_version = 1

        if existing_versions:
            version_numbers = [int(str(v).split('v')[-1]) for v in existing_versions]
            next_version = max(version_numbers) + 1

        version_dir = output_dir / f'student_v{next_version}'
        version_dir.mkdir(exist_ok=True)

        logger.info(f"Directory structure created successfully:")
        logger.info(f"Script directory: {script_dir}")
        logger.info(f"Output directory: {output_dir}")
        logger.info(f"Version directory: {version_dir}")

        return version_dir

    except OSError as e:
        logger.error(f"Failed to create directory structure: {str(e)}")
        raise

def generate_student_data() -> pd.DataFrame:
    """
    Generate synthetic student data with sequential student IDs and realistic names.
    """
    majors = ['Computer Science', 'Business', 'Engineering']  # Reduced to 3 majors
    students = []
    current_year = 2024

    # Distribution of students across years (increasing)
    year_distribution = {
        current_year - 2: 60,  # Third year: 60 students
        current_year - 1: 65,  # Second year: 65 students
        current_year: 75       # First year: 75 students
    }

    student_count = 1
    for entry_year, count in year_distribution.items():
        for _ in range(count):
            student_id = f"ST{student_count:03d}"
            students.append({
                'student_id': student_id,
                'first_name': fake.first_name(),
                'last_name': fake.last_name(),
                'major': random.choice(majors),
                'entry_year': entry_year
            })
            student_count += 1

    return pd.DataFrame(students)

def generate_courses() -> pd.DataFrame:
    """
    Generate course data with meaningful course IDs and progression.
    Each major has 10 core courses distributed across 3 years (4-3-3 distribution).
    10 electives are available for students to choose from.
    """
    major_codes = {
        'Computer Science': 'CSC',
        'Business': 'BUS',
        'Engineering': 'ENG'
    }

    courses = []

    # Course distribution per year: 4-3-3
    year_distribution = {1: 4, 2: 3, 3: 3}  # 10 core courses total

    # Generate core courses for each major
    for major, code in major_codes.items():
        course_names = {
            'Computer Science': [
                'Programming Fundamentals', 'Data Structures', 'Computer Architecture', 'Discrete Mathematics',  # Year 1
                'Algorithms', 'Database Systems', 'Operating Systems',  # Year 2
                'Software Engineering', 'Computer Networks', 'AI & Machine Learning'  # Year 3
            ],
            'Business': [
                'Business Fundamentals', 'Accounting Principles', 'Marketing Basics', 'Business Economics',  # Year 1
                'Financial Management', 'Operations Management', 'Business Strategy',  # Year 2
                'International Business', 'Business Analytics', 'Corporate Finance'  # Year 3
            ],
            'Engineering': [
                'Engineering Mathematics', 'Physics for Engineers', 'Engineering Design', 'Materials Science',  # Year 1
                'Thermodynamics', 'Mechanics', 'Control Systems',  # Year 2
                'Engineering Ethics', 'Project Management', 'Advanced Design'  # Year 3
            ]
        }

        course_num = 1
        for year, count in year_distribution.items():
            base_number = year * 100
            for i in range(count):
                courses.append({
                    'course_id': f'{code}{base_number + course_num}',
                    'course_name': course_names[major][course_num - 1],
                    'major': major,
                    'course_type': 'Core',
                    'year_level': year,
                    'credits': 3
                })
                course_num += 1

    # Generate 10 electives with varied focus areas
    electives = [
        {'code': 'ART', 'name': 'Art History'},
        {'code': 'COM', 'name': 'Public Speaking'},
        {'code': 'PHI', 'name': 'Critical Thinking'},
        {'code': 'PSY', 'name': 'Psychology'},
        {'code': 'SOC', 'name': 'Sociology'},
        {'code': 'LIT', 'name': 'World Literature'},
        {'code': 'ENV', 'name': 'Environmental Studies'},
        {'code': 'MUS', 'name': 'Music Appreciation'},
        {'code': 'LAN', 'name': 'Foreign Language'},
        {'code': 'ETH', 'name': 'Ethics and Society'}
    ]

    for elective in electives:
        courses.append({
            'course_id': f'{elective["code"]}101',
            'course_name': f'{elective["name"]}',
            'major': 'Elective',
            'course_type': 'Elective',
            'year_level': 1,  # All electives available from year 1
            'credits': 3
        })

    return pd.DataFrame(courses)

def generate_enrollments(students_df: pd.DataFrame, courses_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate enrollment data with exactly 2 courses per semester.
    Students take core courses first, then electives to complete their requirements.
    """
    enrollments = []
    enrollment_id = 1
    latest_semester = '2024-02'

    for _, student in students_df.iterrows():
        major_courses = courses_df[courses_df['major'] == student['major']].sort_values('year_level')
        electives = courses_df[courses_df['course_type'] == 'Elective']
        years_enrolled = 2024 - student['entry_year']

        # Track core courses taken
        core_courses_taken = []
        
        # For each year of enrollment
        for year in range(years_enrolled+1):
            for semester_num, semester in enumerate(['Fall', 'Spring']):
                year_level = year + 1
                semester_code = '01' if semester == 'Fall' else '02'
                semester_name = f'{student["entry_year"] + year}-{semester_code}'

                # Available core courses for this year level
                available_core = major_courses[
                    (major_courses['year_level'] == year_level) & 
                    (~major_courses['course_id'].isin(core_courses_taken))
                ]

                # If we have available core courses, prioritize them
                if len(available_core) >= 2:
                    semester_courses = available_core.sample(n=2)
                elif len(available_core) == 1:
                    # Take one core and one elective
                    core_course = available_core.sample(n=1)
                    available_electives = electives[~electives['course_id'].isin(core_courses_taken)]
                    elective_course = available_electives.sample(n=1)
                    semester_courses = pd.concat([core_course, elective_course])
                else:
                    # Take two electives
                    available_electives = electives[~electives['course_id'].isin(core_courses_taken)]
                    semester_courses = available_electives.sample(n=2)

                # Record the courses taken
                core_courses_taken.extend(semester_courses['course_id'].tolist())

                for _, course in semester_courses.iterrows():
                    status = 'In Progress' if semester_name == latest_semester else \
                            random.choices(['Completed', 'Dropped'], weights=[0.97, 0.03], k=1)[0]

                    enrollments.append({
                        'enrollment_id': f'E{str(enrollment_id).zfill(4)}',
                        'student_id': student['student_id'],
                        'course_id': course['course_id'],
                        'semester': semester_name,
                        'enrollment_date': datetime(
                            student['entry_year'] + year,
                            8 if semester == 'Fall' else 1,
                            random.randint(1, 28)
                        ),
                        'status': status
                    })
                    enrollment_id += 1

    return pd.DataFrame(enrollments)

def generate_academic_performance(enrollments_df: pd.DataFrame) -> pd.DataFrame:
    """
    Generate academic performance data for enrollments.
    """
    performance_data = []
    performance_id = 1

    for _, enrollment in enrollments_df.iterrows():
        if enrollment['status'] == 'Dropped':
            performance_data.append({
                'performance_id': f'P{str(performance_id).zfill(4)}',
                'student_id': enrollment['student_id'],
                'course_id': enrollment['course_id'],
                'grade_point': 0.0,
                'letter_grade': 'F',
                'attendance_rate': round(random.uniform(0.0, 0.5), 2)
            })
        elif enrollment['status'] == 'In Progress':
            performance_data.append({
                'performance_id': f'P{str(performance_id).zfill(4)}',
                'student_id': enrollment['student_id'],
                'course_id': enrollment['course_id'],
                'grade_point': 0.0,
                'letter_grade': 'IP',
                'attendance_rate': round(random.uniform(0.8, 1.0), 2)
            })
        else:  # Completed
            grade_point = random.uniform(2.0, 4.0)
            letter_grade = 'A' if grade_point >= 3.7 else 'B' if grade_point >= 2.7 else 'C' if grade_point >= 1.7 else 'D'
            
            performance_data.append({
                'performance_id': f'P{str(performance_id).zfill(4)}',
                'student_id': enrollment['student_id'],
                'course_id': enrollment['course_id'],
                'grade_point': round(grade_point, 2),
                'letter_grade': letter_grade,
                'attendance_rate': round(random.uniform(0.8, 1.0), 2)
            })
        
        performance_id += 1

    return pd.DataFrame(performance_data)

def validate_data(
    students_df: pd.DataFrame,
    courses_df: pd.DataFrame,
    enrollments_df: pd.DataFrame,
    performance_df: pd.DataFrame,
    activities_df: pd.DataFrame
) -> None:
    """
    Validate generated data for consistency and completeness.
    """
    try:
        # Check for duplicate IDs
        if students_df['student_id'].duplicated().any():
            raise DataValidationError("Duplicate student IDs found")

        if courses_df['course_id'].duplicated().any():
            raise DataValidationError("Duplicate course IDs found")

        # Check foreign key relationships
        student_ids = set(students_df['student_id'])
        course_ids = set(courses_df['course_id'])

        if not set(enrollments_df['student_id']).issubset(student_ids):
            raise DataValidationError("Invalid student IDs in enrollments")

        if not set(enrollments_df['course_id']).issubset(course_ids):
            raise DataValidationError("Invalid course IDs in enrollments")

        if not (0 <= performance_df['attendance_rate'].max() <= 1.0):
            raise DataValidationError("Invalid attendance rate values")

        logger.info("Data validation completed successfully")

    except Exception as e:
        logger.error(f"Data validation failed: {str(e)}")
        raise

def main():
    """
    Main function to orchestrate the data generation process.
    """
    try:
        logger.info("Starting data generation process...")

        # Setup directories
        output_dir = setup_directories()

        # Generate all datasets
        logger.info("Generating student data...")
        students_df = generate_student_data()

        logger.info("Generating course data...")
        courses_df = generate_courses()

        logger.info("Generating enrollment data...")
        enrollments_df = generate_enrollments(students_df, courses_df)

        logger.info("Generating academic performance data...")
        performance_df = generate_academic_performance(enrollments_df)

        # Validate data
        logger.info("Validating generated data...")
        validate_data(students_df, courses_df, enrollments_df, performance_df, pd.DataFrame())

        # Save datasets
        logger.info("Saving datasets...")
        students_df.to_csv(output_dir / 'blackwood_academy__students.csv', index=False)
        courses_df.to_csv(output_dir / 'blackwood_academy__courses.csv', index=False)
        enrollments_df.to_csv(output_dir / 'blackwood_academy__enrollments.csv', index=False)
        performance_df.to_csv(output_dir / 'blackwood_academy__academic_performance.csv', index=False)

        logger.info("Data generation completed successfully!")
        logger.info("Created/Modified files during execution:")
        for file in output_dir.glob('*.csv'):
            logger.info(f"- {file.name}")

    except Exception as e:
        logger.error(f"Error occurred during execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()