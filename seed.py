import psycopg2
import json

def migrate_data():
    # Load data from JSON file
    with open('dashboard_data.json') as f:
        data = json.load(f)

    # Connect to your PostgreSQL database
    conn = psycopg2.connect(
        dbname='DB_NAME',
        user='USER_NAME',
        password='YOUR_PASSWORD',
        host='localhost',
        port='5432'
    )

    # Create a cursor object using the connection
    cur = conn.cursor()

    # Migrate teacher_activities
    for activity in data['teacher_activities']:
        cur.execute("""
            INSERT INTO teacher_activities (teacher_id, name, last_active, activity_score, student_interaction_rating, subjects_taught)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            activity['teacher_id'],
            activity['name'],
            activity['last_active'],
            activity['activity_score'],
            activity['student_interaction_rating'],
            activity['subjects_taught']
        ))

    # Migrate student_progress
    for progress in data['student_progress']:
        cur.execute("""
            INSERT INTO student_progress (class_id, subject, average_score_improvement, homework_completion_rate, attendance_rate)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            progress['class_id'],
            progress['subject'],
            progress['average_score_improvement'],
            progress['homework_completion_rate'],
            progress['attendance_rate']
        ))

    # Migrate resource_management
    for resource in data['resource_management']:
        cur.execute("""
            INSERT INTO resource_management (resource_id, resource_name, allocated_teachers, utilization_rate)
            VALUES (%s, %s, %s, %s)
        """, (
            resource['resource_id'],
            resource['resource_name'],
            resource['allocated_teachers'],
            resource['utilization_rate']
        ))

    # Migrate coach_details
    for coach in data['coach_details']:
        cur.execute("""
            INSERT INTO coach_details (coach_id, name, specialization, years_of_experience)
            VALUES (%s, %s, %s, %s)
        """, (
            coach['coach_id'],
            coach['name'],
            coach['specialization'],
            coach['years_of_experience']
        ))

    # Migrate coach_teacher_interactions
    for interaction in data['coach_teacher_interactions']:
        cur.execute("""
            INSERT INTO coach_teacher_interactions (coach_id, teacher_id, last_meeting_date, meeting_notes)
            VALUES (%s, %s, %s, %s)
        """, (
            interaction['coach_id'],
            interaction['teacher_id'],
            interaction['last_meeting_date'],
            interaction['meeting_notes']
        ))

    # Commit the changes
    conn.commit()

    # Close cursor and connection
    cur.close()
    conn.close()

# Call the migration function
migrate_data()
