import os

from kivy.graphics import Color, Line, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App

Builder.load_file('kv/dailyquizscreen.kv')

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '../../db/UserActivities.db')

'''
Daily quiz screen loads up daily quiz and takes in user activity data and stores it within the SQLite database
'''
class DailyQuizScreen(Screen):

    '''
    Checks to see if quiz already complete, if not runs quiz
    '''
    def on_enter(self):
        if not App.get_running_app().daily_quiz_comp():
            print('quiz complete')
            App.get_running_app().show_popup("You have already completed the quiz today.")
            self.manager.current = 'home'
            return
        #super(DailyQuizScreen, self).on_enter()  # Ensure the superclass method is called
        self.update_content()

    '''
    Updates to next question in quiz
    '''

    def update_content(self):
        self.ids.answers_container.clear_widgets()
        question = self.manager.get_current_question()
        self.ids.question_label.text = question['question']
        for answer in question['answers']:
            btn = Button(text=answer)
            self.style_button(btn)
            btn.bind(on_release=self.advance_quiz)
            self.ids.answers_container.add_widget(btn)

    '''
    Button style setting
    '''

    def style_button(self, button):
        button.font_name = 'assets/font.ttf'
        button.bold = True
        button.size_hint_y = None
        button.height = dp(40)
        button.background_normal = ''
        button.background_color = 0.086, 0.341, 0.459, 1
        button.color = 1, 1, 1, 1
        button.border = (4, 4, 4, 4)

    '''
    Advances page to next question
    '''
    def advance_quiz(self, instance):
        question = self.manager.get_current_question()
        user_answer = instance.text
        App.get_running_app().update_activities(question['activity'], user_answer)

        self.manager.next_question()
        self.update_content()