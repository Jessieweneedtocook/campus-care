import os
import textwrap
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
import sqlite3
import requests
from kivy.lang import Builder
from kivy.base import EventLoop
from kivy.app import App

# Set the working directory to the root of your project
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from CampCareFE.app import MyApp
from CampCareFE.screens.signup import SignupScreen
from CampCareFE.screens.wellness_progress import WellnessProgressScreen

# Initialize Kivy environment for testing
if not App.get_running_app():
    EventLoop.ensure_window()

class TestMyApp(unittest.TestCase):

    @patch('sqlite3.connect')
    def test_database_creation_on_init(self, mock_connect): #passes
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        app = MyApp()
        app.build()
        mock_cursor.execute.assert_any_call("""
            CREATE TABLE IF NOT EXISTS UserActivities (
                ActivityID INTEGER PRIMARY KEY AUTOINCREMENT,
                UserID INTEGER NOT NULL,
                ActivityType TEXT NOT NULL,
                TimeSpent INTEGER,
                ActivityDate DATETIME NOT NULL
            )
        """)

    def test_screen_transitions(self): #passes
        app = MyApp()
        app.build()
        app.sm.current = 'login'
        self.assertEqual(app.sm.current, 'login')
        app.sm.current = 'home'
        self.assertEqual(app.sm.current, 'home')

    @patch('sqlite3.connect')
    def test_fetch_and_update_user_preferences(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = (['running', 'swimming'],)  # Note: Tuple of list
        app = MyApp()
        result = app.fetch_preferences(user_id=1)
        self.assertEqual(result, ['running', 'swimming'])
        app.selected_activities = ['yoga']
        app.update_preferences(user_id=1)
        mock_cursor.execute.assert_called_with("""
            UPDATE UserActivityPreferences
            SET Activities = ?
            WHERE UserID = ?
            """, (str(['yoga']), 1))

    def test_filtering_quiz_questions(self):
        app = MyApp()
        app.selected_activities = ['Sleeping']
        app.sm.current_question_index = 0
        question = app.get_filtered_question()
        print("Selected Activities:", app.selected_activities)
        print("Filtered Question:", question)
        self.assertEqual(question.get('activity'), 'Sleeping', f"Expected: 'Sleeping', Got: {question.get('activity')}")

    @patch('sqlite3.connect')
    def test_daily_quiz_completion_check(self, mock_connect): #passes
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        app = MyApp()
        result = app.daily_quiz_comp(user_id=1)
        self.assertTrue(result)

    @patch('sqlite3.connect')
    def test_handle_empty_user_preferences(self, mock_connect): #passes
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        app = MyApp()
        result = app.fetch_preferences(user_id=1)
        self.assertEqual(result, [])

    @patch('sqlite3.connect')
    def test_no_data_returned_from_db_queries(self, mock_connect): #passes
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = []
        screen = WellnessProgressScreen()
        data_by_activity_type = screen.get_data_for_period(7)
        self.assertEqual(data_by_activity_type, {})

    @patch('requests.post', side_effect=requests.exceptions.RequestException)
    def test_external_api_failure_during_signup(self, mock_post): #passes
        app = MyApp()
        screen = SignupScreen()
        result = screen.send_to_server(user_data={'username': 'testuser'})
        self.assertFalse(result)

    @patch('sqlite3.connect')
    def test_handle_non_existent_user_ids(self, mock_connect): #passes
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        app = MyApp()
        result = app.fetch_preferences(user_id=999)
        self.assertEqual(result, [])

    def test_no_selected_activities_for_quiz(self): #passes
        app = MyApp()
        app.selected_activities = []
        app.sm = MagicMock()
        app.sm.current_question_index = 0
        question = app.get_filtered_question()
        self.assertEqual(question, {})

    @patch('kivy.uix.popup.Popup.open')
    def test_popup_display_functionality(self, mock_open): #passes
        app = MyApp()
        app.show_popup("Test Message")
        mock_open.assert_called_once()

if __name__ == '__main__':
    unittest.main()
