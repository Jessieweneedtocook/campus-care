import os
import unittest
from unittest.mock import patch, MagicMock

import requests
from kivy.base import EventLoop
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from CampCareFE.app import MyApp
from CampCareFE.screens.signup import SignupScreen
from CampCareFE.screens.wellness_progress import WellnessProgressScreen
from CampCareFE.quiz_questions import questions
from CampCareFE.screens.daily_quiz import DailyQuizScreen
from CampCareFE.screens.home import HomeScreen

# Set the working directory to the root of your project
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Kivy environment for testing
if not App.get_running_app():
    EventLoop.ensure_window()

class TestMyApp(unittest.TestCase):
    def test_increment_current_question_index(self): #passes
        my_app = MyApp()
        my_app.selected_activities = ['Socialisation', 'Sleeping']
        my_app.sm = ScreenManager()
        # Add the "home" screen to the ScreenManager
        home_screen = HomeScreen(name='home')
        my_app.sm.add_widget(home_screen)
        my_app.sm.current_question_index = 0
        my_app.sm.add_widget(DailyQuizScreen(name='dailyquiz'))

    def test_question_index_resets(self): #passes
        app = MyApp()
        app.sm = ScreenManager()  # Initialize the screen manager
        app.selected_activities = ['Socialisation', 'Sleeping']

        # Ensure there are questions for the selected activities
        selected_questions = [q for q in questions if q['activity'] in app.selected_activities]
        self.assertGreater(len(selected_questions), 0, "No questions for the selected activities")

        # Set the current_question_index to the last question
        app.sm.current_question_index = len(selected_questions) - 1

    def test_screen_transitions(self): #passes
        app = MyApp()
        app.build()
        app.sm.current = 'login'
        self.assertEqual(app.sm.current, 'login')
        app.sm.current = 'home'
        self.assertEqual(app.sm.current, 'home')

    @patch('sqlite3.connect')
    def test_daily_quiz_completion_check(self, mock_connect): #passes
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        app = MyApp()
        result = app.daily_quiz_comp()
        self.assertTrue(result)

    @patch('sqlite3.connect')
    def test_handle_empty_user_preferences(self, mock_connect): #passes
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        app = MyApp()
        result = app.fetch_preferences()
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
        result = app.fetch_preferences()
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


class TestSignupScreen(unittest.TestCase):
    def test_valid_user_data_sent_successfully(self):
        sm = ScreenManager()
        signup_screen = SignupScreen(name='signup')
        sm.add_widget(signup_screen)
        sm.current = 'signup'

        signup_screen.ids = {
            'username_input': type('Mock', (object,), {'text': 'testuser'}),
            'email_input': type('Mock', (object,), {'text': 'test@example.com'}),
            'number_input': type('Mock', (object,), {'text': '1234567890'}),
            'dob_input': type('Mock', (object,), {'text': '01/01/1990'}),
            'password_input': type('Mock', (object,), {'text': 'password123'}),
            'confirm_password_input': type('Mock', (object,), {'text': 'password123'}),
            'error_message': type('Mock', (object,), {'text': ''})
        }

        with patch.object(SignupScreen, 'send_to_server', return_value=False) as mock_send_to_server:
            signup_screen.submit_signup_data()
            mock_send_to_server.assert_called_once()
            self.assertNotEqual(sm.current, 'initialoptions')
            self.assertNotEqual(signup_screen.ids.error_message.text, '')

    #  method returns True when server responds with status code 200
    def test_send_to_server_success(self):
        user_data = {
            "username": "test_user",
            "email": "test_user@example.com",
            "phone": "1234567890",
            "dob": "01/01/2000",
            "password": "password123",
            "confirm_password": "password123"
        }
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            signup_screen = SignupScreen()
            result = signup_screen.send_to_server(user_data)
            self.assertTrue(result)


class TestDailyQuizScreen(unittest.TestCase):
    def test_on_enter_quiz_completion_check(self):
        with patch.object(App, 'get_running_app') as mock_app:
            mock_app.return_value.daily_quiz_comp.return_value = False
            screen = DailyQuizScreen()
            screen.manager = MagicMock()
            screen.on_enter()
            mock_app.return_value.daily_quiz_comp.assert_called_once_with()
            mock_app.return_value.show_popup.assert_called_once_with("You have already completed the quiz today.")
            self.assertEqual(screen.manager.current, 'home')

    def test_update_content_populates_correctly(self):
        screen = DailyQuizScreen()
        screen.ids = {'answers_container': MagicMock(), 'question_label': MagicMock()}
        screen.manager = MagicMock()
        screen.manager.get_current_question.return_value = {'question': 'What is your favorite color?', 'answers': ['Red', 'Blue', 'Green']}
        screen.update_content()
        self.assertEqual(screen.ids.question_label.text, 'What is your favorite color?')
        self.assertEqual(len(screen.ids.answers_container.add_widget.call_args_list), 3)
        for call, answer in zip(screen.ids.answers_container.add_widget.call_args_list, ['Red', 'Blue', 'Green']):
            self.assertIsInstance(call[0][0], Button)
            self.assertEqual(call[0][0].text, answer)

    def test_handle_corrupted_quiz_data(self):
        screen = DailyQuizScreen()
        screen.ids = {'answers_container': MagicMock(), 'question_label': MagicMock()}
        screen.manager = MagicMock()
        screen.manager.get_current_question.return_value = {'question': None,
                                                            'answers': []}  # Change 'answers' to an empty list
        screen.update_content()
        self.assertIsNone(screen.ids.question_label.text)
        self.assertEqual(screen.ids.answers_container.add_widget.call_count, 0)

    #  Test behavior when the user's ID is invalid or not found
    def test_invalid_user_id_behavior(self):
        with patch.object(App, 'get_running_app') as mock_app:
            mock_app.return_value.daily_quiz_comp.return_value = True
            mock_app.return_value.update_activities.side_effect = Exception("Invalid user ID")
            screen = DailyQuizScreen()
            screen.manager = MagicMock()
            button = MagicMock(text='Yes')
            with self.assertRaises(Exception) as context:
                screen.advance_quiz(button)
            self.assertIn("Invalid user ID", str(context.exception))

if __name__ == '__main__':
    unittest.main()
