import sqlite3
from datetime import datetime, timedelta
import random


conn = sqlite3.connect('UserActivities.db')
cursor = conn.cursor()

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserActivities (
            ActivityID INTEGER PRIMARY KEY AUTOINCREMENT,
            ActivityType TEXT NOT NULL,
            TimeSpent TEXT,
            ActivityDate DATETIME NOT NULL
        )
    """)

def generate_sample_data():
    activity_types = ['Sleeping', 'Hobbies', 'Exercise', 'Work', 'Social']
    time_spent_categories = ['Less than 1', '1-3', 'More than 4', 'Less than 5']
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2024, 5, 30)
    delta_days = (end_date - start_date).days

    # Generate data for the past 2 weeks
    recent_data = []
    today = datetime.now()
    for _ in range(14):  # 14 days for the past 2 weeks
        activity_type = random.choice(activity_types)
        time_spent = random.choice(time_spent_categories)
        activity_date = today - timedelta(days=14 - _) + timedelta(seconds=random.randint(0, 86399))
        recent_data.append((activity_type, time_spent, activity_date))

    # Generate additional historical data
    historical_data = []
    for _ in range(1000 - 14):  # Assuming 1000 sample records
        activity_type = random.choice(activity_types)
        time_spent = random.choice(time_spent_categories)
        activity_date = start_date + timedelta(days=random.randint(0, delta_days), seconds=random.randint(0, 86399))
        historical_data.append((activity_type, time_spent, activity_date))

    return recent_data, historical_data

def insert_sample_data(cursor, sample_data):
    recent_data, historical_data = sample_data
    cursor.executemany("""
        INSERT INTO UserActivities (ActivityType, TimeSpent, ActivityDate)
        VALUES (?, ?, ?)
    """, recent_data + historical_data)

def main():
    # Create the UserActivities table
    create_table(cursor)

    # Generate sample data
    sample_data = generate_sample_data()

    # Insert sample data into the UserActivities table
    insert_sample_data(cursor, sample_data)

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

    print("Sample data inserted into the UserActivities table successfully.")

if __name__ == "__main__":
    main()
