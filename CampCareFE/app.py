from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from datetime import datetime
import sqlite3

# Import screens
from CampCareFE.screens.daily_quiz import db_path, DailyQuizScreen
from screens.login import LoginScreen
from screens.signup import SignupScreen
from screens.reset_password import ResetPasswordScreen
from screens.home import HomeScreen
from screens.wellness_progress import WellnessProgressScreen
from screens.user_info import UserInfoScreen
from screens.initial_options import InitialOptionsScreen
from screens.wellness_help import WellnessHelpScreen
from screens.options import OptionsScreen
from screens.admin import AdminScreen
from screens.wellness_schedule import WellnessScheduleScreen
from kivy.core.window import Window
from quiz_questions import questions


class MyApp(App):

    role = None
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.questions = questions
        self.access_token = None

    def build(self):
        # Create the database if not exists
        self.create_database()

        # Set window size
        Window.size = (375, 667)
        self.questions = questions
        # Fetch user preferences
        self.selected_activities = self.fetch_preferences()
        self.selected_activities = [activity.strip("'") for activity in self.selected_activities]

        # Initialize ScreenManager
        self.sm = ScreenManager()
        self.plot_graph()
        # Add screens to ScreenManager
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(SignupScreen(name='signup'))
        self.sm.add_widget(ResetPasswordScreen(name='resetpassword'))
        self.sm.add_widget(HomeScreen(name='home'))
        self.sm.add_widget(WellnessProgressScreen(name='wellnessprogress'))
        self.sm.add_widget(UserInfoScreen(name='userinfo'))
        self.sm.add_widget(InitialOptionsScreen(name='initialoptions'))
        self.sm.add_widget(WellnessHelpScreen(name='wellnesshelp'))
        self.sm.add_widget(OptionsScreen(name='options'))
        self.sm.add_widget(AdminScreen(name='admin'))
        self.sm.add_widget(WellnessScheduleScreen(name='wellnessschedule'))
        self.sm.add_widget(DailyQuizScreen(name='dailyquiz'))

        # Initialize quiz related attributes
        self.sm.current_question_index = 0
        self.sm.get_current_question = self.get_filtered_question
        self.sm.next_question = self.next_question
        self.sm.current = 'login'

        # Flag to track if all questions have been asked
        self.all_questions_asked = False

        # Return ScreenManager
        return self.sm

    def fetch_preferences(self):
        # Fetch user activity preferences from the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = "SELECT Activities FROM UserActivityPreferences"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()

        if result is not None:
            # Convert the string of activities back into a list
            return result[0].strip('][').split(', ')
        else:
            return []

    def get_filtered_question(self):
        # Get filtered questions based on user's selected activities
        selected_activities = [activity.strip("'") for activity in self.selected_activities]
        filtered_questions = [q for q in questions if q['activity'] in selected_activities]

        if self.sm.current_question_index < len(filtered_questions):
            question = filtered_questions[self.sm.current_question_index]
            question['index'] = self.sm.current_question_index
            return question
        return {}

    def next_question(self, instance=None):
        # Move to the next question in the quiz
        filtered_questions = [q for q in questions if q['activity'] in self.selected_activities]

        if self.sm.current_question_index < len(filtered_questions) - 1:
            self.sm.current_question_index += 1
            self.sm.get_screen('dailyquiz').update_content()
            self.sm.current = 'dailyquiz'
        else:
            self.sm.current = 'home'
            self.sm.current_question_index = 0

    def save_preferences(self):
        # Save user activity preferences to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
                INSERT INTO UserActivityPreferences (Activities)
                VALUES (?)
                """
        data = (str(self.selected_activities),)
        cursor.execute(query, data)
        conn.commit()
        conn.close()

    def update_preferences(self):
        # Update user activity preferences in the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
                UPDATE UserActivityPreferences
                SET Activities = ?
                """
        data = (str(self.selected_activities),)
        cursor.execute(query, data)
        conn.commit()
        conn.close()

    def create_database(self):
        # Create necessary tables in the database if they don't exist
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserActivities (
                ActivityID INTEGER PRIMARY KEY AUTOINCREMENT,
                ActivityType TEXT NOT NULL,
                TimeSpent INTEGER,
                ActivityDate DATETIME NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserActivityPreferences (
                PreferenceID INTEGER PRIMARY KEY AUTOINCREMENT,
                Activities TEXT
            )
        """)

        conn.commit()
        conn.close()

    def update_activities(self, activity_type, user_answer):
        # Update user activities in the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
        INSERT INTO UserActivities (ActivityType, TimeSpent, ActivityDate)
        VALUES (?, ?, ?)
        """
        data = (activity_type, user_answer, datetime.now())
        cursor.execute(query, data)
        conn.commit()
        conn.close()

    def plot_graph(self):
        # Plot graphs for wellness progress
        screen = WellnessProgressScreen()
        screen.plot_stats()
        screen.overall_progress()

    def daily_quiz_comp(self):
        # Check if daily quiz is completed
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        query = """
            SELECT * FROM UserActivities
            WHERE Date(ActivityDate) = ?
            """
        current_date = datetime.now().date().isoformat()
        cursor.execute(query, (current_date,))
        entry = cursor.fetchone()
        conn.close()

        return entry is None

    def show_popup(self, message):
        # Show a popup with given message
        popup = Popup(title='Info', content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def set_access_token(self, token):
        # Set access token for authentication
        self.access_token = token

    def set_role(self, role):
        self.role = role

    def get_role(self):
        return self.role

    def logout(self):
        # Logout user
        self.access_token = None
        self.sm.current = 'login'
