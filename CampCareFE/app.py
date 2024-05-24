from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
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

    def build(self):
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

        self.sm.current_question_index = 0
        self.selected_activities = []
        self.sm.get_current_question = self.get_filtered_question
        self.sm.next_question = self.next_question

        self.sm.current_question_index = 0
        self.sm.get_current_question = lambda: questions[self.sm.current_question_index]
        self.sm.next_question = self.next_question
        self.sm.add_widget(DailyQuizScreen(name='dailyquiz'))
        self.sm.current = 'login'
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
            self.sm.current = 'dailyquiz'
        else:
            self.sm.current = 'home'




    def next_question(self, instance=None):
        if self.sm.current_question_index < len(questions) - 1:
            self.sm.current_question_index += 1
            self.sm.current = 'dailyquiz'
        else:
            self.sm.current = 'login'

