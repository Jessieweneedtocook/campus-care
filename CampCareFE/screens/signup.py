from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from users.form import SignupForm

Builder.load_file('kv/signupscreen.kv')


class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signup_form = SignupForm()

    def sign_up(self):
        self.signup_form.username.data = self.ids.username_input.text
        self.signup_form.email.data = self.ids.email_input.text
        self.signup_form.phone.data = self.ids.phone_input.text
        self.signup_form.dob.data = self.ids.dob_input.text
        self.signup_form.password.data = self.ids.password_input.text
        self.signup_form.confirm_password.data = self.ids.confirm_password_input.text


