import os
import unittest
from unittest.mock import patch, MagicMock

import requests
from kivy.base import EventLoop
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.button import Button
from CampCareFE.app import MyApp
from CampCareFE.screens.admin import SuccessPopup, DeleteAccountPopup
from CampCareFE.screens.initial_options import InitialOptionsScreen
from CampCareFE.screens.options import OptionsScreen
from CampCareFE.screens.signup import SignupScreen
from CampCareFE.screens.user_info import UserInfoScreen
from CampCareFE.screens.wellness_progress import WellnessProgressScreen
from CampCareFE.quiz_questions import questions
from CampCareFE.screens.daily_quiz import DailyQuizScreen, db_path
from CampCareFE.screens.home import HomeScreen

# Set the working directory to the root of your project
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize Kivy environment for testing
if not App.get_running_app():
    EventLoop.ensure_window()

class TestMyApp(unittest.TestCase):
    def test_increment_current_question_index(self):
        my_app = MyApp()
        my_app.selected_activities = ['Socialisation', 'Sleeping']
        my_app.sm = ScreenManager()
        # Add the "home" screen to the ScreenManager
        home_screen = HomeScreen(name='home')
        my_app.sm.add_widget(home_screen)
        my_app.sm.current_question_index = 0
        my_app.sm.add_widget(DailyQuizScreen(name='dailyquiz'))

    def test_question_index_resets(self):
        app = MyApp()
        app.sm = ScreenManager()  # Initialize the screen manager
        app.selected_activities = ['Socialisation', 'Sleeping']

        # Ensure there are questions for the selected activities
        selected_questions = [q for q in questions if q['activity'] in app.selected_activities]
        self.assertGreater(len(selected_questions), 0, "No questions for the selected activities")

        # Set the current_question_index to the last question
        app.sm.current_question_index = len(selected_questions) - 1

    def test_screen_transitions(self):
        app = MyApp()
        app.build()
        app.sm.current = 'login'
        self.assertEqual(app.sm.current, 'login')
        app.sm.current = 'home'
        self.assertEqual(app.sm.current, 'home')

    @patch('sqlite3.connect')
    def test_daily_quiz_completion_check(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        app = MyApp()
        result = app.daily_quiz_comp()
        self.assertTrue(result)

    @patch('sqlite3.connect')
    def test_handle_empty_user_preferences(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        app = MyApp()
        result = app.fetch_preferences()
        self.assertEqual(result, [])

    @patch('sqlite3.connect')
    def test_no_data_returned_from_db_queries(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchall.return_value = []
        screen = WellnessProgressScreen()
        data_by_activity_type = screen.get_data_for_period(7)
        self.assertEqual(data_by_activity_type, {})

    @patch('sqlite3.connect')
    def test_handle_non_existent_user_ids(self, mock_connect):
        mock_conn = mock_connect.return_value
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.fetchone.return_value = None
        app = MyApp()
        result = app.fetch_preferences()
        self.assertEqual(result, [])

    def test_no_selected_activities_for_quiz(self):
        app = MyApp()
        app.selected_activities = []
        app.sm = MagicMock()
        app.sm.current_question_index = 0
        question = app.get_filtered_question()
        self.assertEqual(question, {})

    @patch('kivy.uix.popup.Popup.open')
    def test_popup_display_functionality(self, mock_open):
        app = MyApp()
        app.show_popup("Test Message")
        mock_open.assert_called_once()


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


class TestInitialOptionsScreen(unittest.TestCase):
#  fetch_selected_activities retrieves activities for a valid user ID
    def test_fetch_selected_activities_valid(self):
        import sqlite3
        from unittest.mock import patch, MagicMock
        from CampCareFE.screens.initial_options import InitialOptionsScreen

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = ('[Activity1, Activity2]',)
        mock_conn.cursor.return_value = mock_cursor

        with patch('sqlite3.connect', return_value=mock_conn):
            screen = InitialOptionsScreen()
            activities = screen.fetch_selected_activities()
            self.assertEqual(activities, ['Activity1', 'Activity2'])

    #  fetch_selected_activities handles with no activities
    def test_fetch_selected_activities_no_activities(self):
        from unittest.mock import patch, MagicMock
        from CampCareFE.screens.initial_options import InitialOptionsScreen

        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = None
        mock_conn.cursor.return_value = mock_cursor

        with patch('sqlite3.connect', return_value=mock_conn):
            screen = InitialOptionsScreen()
            activities = screen.fetch_selected_activities()
            self.assertEqual(activities, [])

class TestOptionsScreen(unittest.TestCase):
    def test_toggle_activity_adds_activity(self):
        from kivy.uix.button import Button
        screen = OptionsScreen()
        button = Button(text='Activity1', state='down')
        screen.toggle_activity(button)
        self.assertIn('Activity1', screen.get_selected_activities())

    def test_toggle_activity_remove_activity(self):
        from kivy.uix.button import Button
        screen = OptionsScreen()
        button = Button(text='Activity1', state='down')
        screen.toggle_activity(button)
        button.state = 'normal'
        screen.toggle_activity(button)
        self.assertNotIn('Activity1', screen.get_selected_activities())


class TestingAdmin(unittest.TestCase):
    def test_popup_displays_with_correct_title(self):
        from kivy.uix.label import Label
        message = "Test message"
        popup = SuccessPopup(message)
        self.assertEqual(popup.title, "Success")
        self.assertIn(message, [child.text for child in popup.content.children if isinstance(child, Label)])

    def test_successfully_deletes_user(self):
        from kivy.app import App
        from unittest.mock import patch, MagicMock
        from CampCareFE.screens.admin import DeleteAccountPopup, SuccessPopup

        class MockApp(App):
            access_token = "mock_token"
            def logout(self):
                pass

        app = MockApp()
        App.get_running_app = MagicMock(return_value=app)

        # Mock the API call to return a valid user list
        with patch('requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'usernames': ['valid_user']}
            mock_post.return_value = mock_response

            popup = DeleteAccountPopup()
            popup.user_to_delete_input.text = "valid_user"

            # Mock the delete user API call
            with patch('requests.post') as mock_post_delete:
                mock_response_delete = MagicMock()
                mock_response_delete.status_code = 200
                mock_response_delete.json.return_value = {}
                mock_post_delete.return_value = mock_response_delete

                with patch.object(SuccessPopup, 'open', return_value=None) as mock_success_open:
                    with patch.object(app, 'logout', return_value=None) as mock_logout:
                        popup.delete_user(None)
                        mock_post_delete.assert_called_once()
                        mock_success_open.assert_called_once()
                        mock_logout.assert_called_once()


if __name__ == '__main__':
    unittest.main()
