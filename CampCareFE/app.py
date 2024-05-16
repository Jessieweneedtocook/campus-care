import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from CampCareFE.screens.daily_quiz import db_path, DailyQuizScreen
from screens.login import LoginScreen
from screens.signup import SignupScreen
from screens.reset_password import ResetPasswordScreen
from kivy.core.window import Window
from quiz_questions import questions

class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.questions = questions

    def build(self):
        self.create_database()

        Window.size = (375, 667)
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(SignupScreen(name='signup'))
        self.sm.add_widget(ResetPasswordScreen(name='resetpassword'))

        self.daily_quiz_screen = DailyQuizScreen(name='dailyquiz')
        self.sm.add_widget(self.daily_quiz_screen)
        self.sm.current_question_index = 0
        self.sm.current = 'login'
        self.all_questions_asked = False  # Flag to track if all questions have been asked
        return self.sm

    def next_question(self):
        if not self.all_questions_asked:
            self.sm.current_question_index += 1
            if self.sm.current_question_index >= len(self.questions):
                self.sm.current_question_index = 0
                self.all_questions_asked = True
                self.sm.current = 'home'
            else:
                self.daily_quiz_screen.update_content(self.sm.current_question_index)

    def create_database(self):
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

    def update_activities(self, user_id, activity_type, user_answer):
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

