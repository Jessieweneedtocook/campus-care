from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.app import App

from CampCareFE.screens.wellness_progress import WellnessProgressScreen

Builder.load_file('kv/homescreen.kv')


class HomeScreen(Screen):
    def on_enter(self):
        screen = WellnessProgressScreen()
        data_by_activity_type = screen.get_data_for_period(7)
        stats_by_activity_type = screen.calculate_stats(data_by_activity_type)
        screen.plot_stats(stats_by_activity_type)
        screen.overall_progress()

    def go_to_daily_quiz(self):
        if App.get_running_app().daily_quiz_comp():
            self.manager.current = 'dailyquiz'
        else:
            App.get_running_app().show_popup("You have already completed the quiz today.")