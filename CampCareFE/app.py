import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from CampCareFE.screens.daily_quiz import db_path, DailyQuizScreen
from screens.login import LoginScreen
from screens.signup import SignupScreen
from screens.reset_password import ResetPasswordScreen
from screens.daily_quiz import DailyQuizScreen
from screens.home import HomeScreen
from screens.wellness_progress import WellnessProgressScreen
from screens.user_info import UserInfoScreen
from screens.initial_options import InitialOptionsScreen
from screens.wellness_help import WellnessHelpScreen
from screens.options import OptionsScreen
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
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(WellnessProgressScreen(name='wellnessprogress'))
        self.sm.add_widget(UserInfoScreen(name='userinfo'))
        self.sm.add_widget(InitialOptionsScreen(name='initialoptions'))
        self.sm.add_widget(WellnessHelpScreen(name='wellnesshelp'))
        self.sm.add_widget(OptionsScreen(name='options'))

        self.daily_quiz_screen = DailyQuizScreen(name='dailyquiz')
        self.sm.add_widget(self.daily_quiz_screen)
        self.sm.current_question_index = 0
        self.selected_activities = []
        self.sm.get_current_question = self.get_filtered_question
        self.sm.next_question = self.next_question
        self.sm.add_widget(DailyQuizScreen(name='dailyquiz'))
        self.sm.current = 'login'
        self.all_questions_asked = False  # Flag to track if all questions have been asked
        return self.sm

    def get_filtered_question(self):
        filtered_questions = [q for q in questions if q['activity'] in self.selected_activities]
        if filtered_questions:
            return filtered_questions[self.sm.current_question_index]
        return None

    def next_question(self, instance=None):
        filtered_questions = [q for q in questions if q['activity'] in self.selected_activities]
        print(self.sm.current_question_index)
        if self.sm.current_question_index < len(filtered_questions) - 1:
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




