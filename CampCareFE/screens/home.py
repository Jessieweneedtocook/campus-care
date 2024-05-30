from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App

from CampCareFE.screens.wellness_progress import WellnessProgressScreen

# Load the corresponding KV file
Builder.load_file('kv/homescreen.kv')

class HomeScreen(Screen):
    """
    Class representing the home screen.
    """
    def on_enter(self):
        """
        Method called when the screen is entered.
        """
        pass

    def go_to_daily_quiz(self):
        """
        Method to navigate to the daily quiz screen.
        """
        if App.get_running_app().daily_quiz_comp():
            # Navigate to the daily quiz screen if the quiz is not completed yet
            self.manager.current = 'dailyquiz'
        else:
            # Show a popup if the quiz is already completed for the day
            App.get_running_app().show_popup("You have already completed the quiz today.")
