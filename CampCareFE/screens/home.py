from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App
Builder.load_file('kv/homescreen.kv')


class HomeScreen(Screen):
    def on_enter(self):
        pass  # Your existing code

    def go_to_daily_quiz(self):
        if App.get_running_app().daily_quiz_comp():
            self.manager.current = 'dailyquiz'
        else:
            App.get_running_app().show_popup("You have already completed the quiz today.")