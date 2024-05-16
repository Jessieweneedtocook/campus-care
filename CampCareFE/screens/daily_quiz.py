import os

from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App


Builder.load_file('kv/dailyquizscreen.kv')

script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '../../db/UserActivities.db')


class DailyQuizScreen(Screen):
    def on_enter(self):
        super(DailyQuizScreen, self).on_enter()  # Ensure the superclass method is called
        self.update_content()

    def update_content(self):
        self.ids.answers_container.clear_widgets()
        question = self.manager.get_current_question()
        self.ids.question_label.text = question['question']
        for answer in question['answers']:
            btn = Button(text=answer)
            btn.bind(on_release=self.advance_quiz)
            self.ids.answers_container.add_widget(btn)

    def advance_quiz(self, instance):
        user_id = 1  # Replace with actual user ID
        question = self.manager.get_current_question()
        user_answer = instance.text
        App.get_running_app().update_activities(user_id, question['question'], user_answer)

        self.manager.next_question()
        self.update_content()
