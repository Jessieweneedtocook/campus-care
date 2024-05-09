from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.lang import Builder


Builder.load_file('kv/dailyquizscreen.kv')


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
        self.manager.next_question()
        self.update_content()
