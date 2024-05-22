import sqlite3
from datetime import datetime

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label

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
        self.questions = questions
        self.selected_activities = self.fetch_preferences(user_id=1)
        self.selected_activities = [activity.strip("'") for activity in self.selected_activities]
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
        #self.selected_activities = []
        self.sm.get_current_question = self.get_filtered_question
        self.sm.next_question = self.next_question
        self.sm.add_widget(DailyQuizScreen(name='dailyquiz'))
        self.sm.current = 'login'
        self.all_questions_asked = False  # Flag to track if all questions have been asked
        return self.sm

    def fetch_preferences(self, user_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
                SELECT Activities FROM UserActivityPreferences WHERE UserID = ?
                """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        conn.close()

        if result is not None:
            # Convert the string of activities back into a list
            return result[0].strip('][').split(', ')
        else:
            return []

    def get_filtered_question(self):
        print(f"Selected activities: {self.selected_activities}")
        # Strip the extra quotes from the selected activities
        selected_activities = [activity.strip("'") for activity in self.selected_activities]
        filtered_questions = [q for q in questions if q['activity'] in selected_activities]
        print(f"Filtered questions: {filtered_questions}")
        if self.sm.current_question_index < len(filtered_questions):
            question = filtered_questions[self.sm.current_question_index]
            question[
                'index'] = self.sm.current_question_index  # Add the current question index to the question dictionary
            return question
        return {}

    def next_question(self, instance=None):
        filtered_questions = [q for q in questions if q['activity'] in self.selected_activities]
        if self.sm.current_question_index < len(filtered_questions) - 1:
            self.sm.current_question_index += 1
            self.sm.get_screen('dailyquiz').update_content()  # Update the content of the 'dailyquiz' screen
            self.sm.current = 'dailyquiz'
        else:
            self.sm.current = 'home'
            self.sm.current_question_index = 0  # Reset the question index for the next quiz

    def save_preferences(self, user_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
                INSERT INTO UserActivityPreferences (UserID, Activities)
                VALUES (?, ?)
                """
        data = (user_id, str(self.selected_activities))
        cursor.execute(query, data)
        conn.commit()
        conn.close()

    def update_preferences(self, user_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
                UPDATE UserActivityPreferences
                SET Activities = ?
                WHERE UserID = ?
                """
        data = (str(self.selected_activities), user_id)
        cursor.execute(query, data)
        conn.commit()
        conn.close()


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

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserActivityPreferences (
                PreferenceID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER,
                Activities TEXT,
                FOREIGN KEY(UserID) REFERENCES Users(UserID)
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

    def plot_graph(self):
        screen = WellnessProgressScreen()
        data_by_activity_type = screen.get_data_for_period(7)
        stats_by_activity_type = screen.calculate_stats(data_by_activity_type)
        screen.plot_stats(stats_by_activity_type)

    def daily_quiz_comp(self, user_id):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
            SELECT * FROM UserActivities
            WHERE UserID = ? AND Date(ActivityDate) = ?
            """
        cursor.execute(query, (user_id, datetime.now().date()))
        entry = cursor.fetchone()
        conn.close()

        return entry is None

    def show_popup(self, message):
        popup = Popup(title='Info',
                      content=Label(text=message),
                      size_hint=(None, None), size=(400, 200))
        popup.open()



