from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens.login import LoginScreen
from screens.signup import SignupScreen
from screens.reset_password import ResetPasswordScreen
from screens.daily_quiz import DailyQuizScreen
from kivy.core.window import Window
from quiz_questions import questions


class MyApp(App):
    def build(self):
        Window.size = (375, 667)
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login'))
        self.sm.add_widget(SignupScreen(name='signup'))
        self.sm.add_widget(ResetPasswordScreen(name='resetpassword'))

        self.sm.current_question_index = 0
        self.sm.get_current_question = lambda: questions[self.sm.current_question_index]
        self.sm.next_question = self.next_question
        self.sm.add_widget(DailyQuizScreen(name='dailyquiz'))
        self.sm.current = 'login'
        return self.sm

    def next_question(self, instance=None):
        if self.sm.current_question_index < len(questions) - 1:
            self.sm.current_question_index += 1
            self.sm.current = 'dailyquiz'
        else:
            self.sm.current = 'login'

