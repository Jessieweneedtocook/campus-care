import os
import sqlite3

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App


Builder.load_file('kv/dailyquizscreen.kv')

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '../../db/UserActivities.db')


class DailyQuizScreen(Screen):
    def on_enter(self):
        super(DailyQuizScreen, self).on_enter()
        self.update_content(self.manager.current_question_index)

    def update_content(self, current_question_index):
        self.ids.answers_container.clear_widgets()
        question = App.get_running_app().questions[current_question_index]
        self.ids.question_label.text = question['question']
        for answer in question['answers']:
            btn = Button(text=answer)
            btn.bind(on_release=self.advance_quiz)
            self.ids.answers_container.add_widget(btn)

    def advance_quiz(self, instance):
        user_id = 1  # Replace with actual user ID
        current_question_index = self.manager.current_question_index
        question = App.get_running_app().questions[current_question_index]
        user_answer = instance.text
        App.get_running_app().update_activities(user_id, question['question'], user_answer)
        App.get_running_app().next_question()
