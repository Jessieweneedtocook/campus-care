import os
import sqlite3

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from datetime import datetime
from kivy.app import App


Builder.load_file('kv/dailyquizscreen.kv')

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '../../db/UserActivities.db')


class DailyQuizScreen(Screen):
    def on_enter(self):
        super(DailyQuizScreen, self).on_enter()  # Ensure the superclass method is called
        self.current_question_index = 0
        self.update_content()

    def update_content(self):
        self.ids.answers_container.clear_widgets()
        question = questions[self.current_question_index]
        self.ids.question_label.text = question['question']
        for answer in question['answers']:
            btn = Button(text=answer)
            btn.bind(on_release=self.advance_quiz)
            self.ids.answers_container.add_widget(btn)

    def advance_quiz(self, instance):
        user_id = 1  # Replace with actual user ID
        question = questions[self.current_question_index]
        user_answer = instance.text  # Get the text of the selected answer
        update_activities(user_id, question['question'], user_answer)  # Update activities in the database
        self.current_question_index += 1  # Move to next question
        if self.current_question_index < len(questions):
            self.update_content()
        else:
            print("Quiz completed!")  # Or perform any action when all questions are answered

def create_database():
    conn = sqlite3.connect(db_path)
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

def update_activities(user_id, activity_type, user_answer):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """
    INSERT INTO UserActivities (UserID, ActivityType, TimeSpent, ActivityDate)
    VALUES (?, ?, ?, ?)
    """
    data = (user_id, activity_type, user_answer, datetime.now())
    cursor.execute(query, data)
    conn.commit()
    conn.close()

# Sample questions for testing
questions = [
    {"question": "Hours spent socialising?", "answers": ["Less than 1", "1-3", "More than 4"]},
    {"question": "Hours spent sleeping", "answers": ["Less than 5", "5-7", "More than 7"]},
    {"question": "Hours spent touching grass?", "answers": ["Less than 1", "1-3", "More than 4"]}
]


# ScreenManager to manage screens
class QuizManager(ScreenManager):
    pass


class MyApp(App):
    def build(self):
        create_database()  # Create the database
        sm = QuizManager()  # Create a ScreenManager
        # Add DailyQuizScreen to the ScreenManager
        sm.add_widget(DailyQuizScreen(name='quiz'))
        return sm


if __name__ == "__main__":
    MyApp().run()
