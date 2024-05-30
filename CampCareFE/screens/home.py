from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App

from CampCareFE.screens.wellness_progress import WellnessProgressScreen

Builder.load_file('kv/homescreen.kv')


class HomeScreen(Screen):
    def on_enter(self):
        pass

    def go_to_daily_quiz(self):
        if App.get_running_app().daily_quiz_comp():
            self.manager.current = 'dailyquiz'
        else:
            App.get_running_app().show_popup("You have already completed the quiz today.")