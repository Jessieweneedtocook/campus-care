from app import MyApp
from quiz_questions import questions
import sqlite3

if __name__ == "__main__":
    MyApp().run()

def create_database():
    conn = sqlite3.connect('UserActivities.db')
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserActivities (
            ActivityID INTEGER PRIMARY KEY AUTOINCREMENT,
            UserID INTEGER NOT NULL,
            ActivityType TEXT NOT NULL,
            TimeSpent INTEGER,
            ActivityDate DATETIME NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def update_activities(user_id, activity_type, time_spent):
    conn = sqlite3.connect('UserActivities.db')
    cursor = conn.cursor()

    query = """
    INSERT INTO UserActivities (UserID, ActivityType, TimeSpent, ActivityDate)
    VALUES (?, ?, ?, ?)
    """
    data = (user_id, activity_type, time_spent, datetime.now())
    cursor.execute(query, data)
    conn.commit()
    conn.close()

def quiz(user_id):
    for question in questions:
        print(question["question"])
        for i, answer in enumerate(question["answers"], start=1):
            print(f"{i}. {answer}")
        user_answer = int(input("Please enter the number of your answer: "))
        time_spent = question["answers"][user_answer - 1]
        update_activities(user_id, question["question"], time_spent)

if __name__ == "__main__":
    create_database()
    user_id = 1  # Replace with actual user ID
    quiz(user_id)