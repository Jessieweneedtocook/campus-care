from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import requests
from kivy.uix.boxlayout import BoxLayout
from users.form import (username_checker,
                        password_checker,
                        phone_checker,
                        dob_checker,
                        confirm_password_checker,
                        email_checker)

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

        url = 'http://localhost:5000/register'
        data = {
            'username': self.ids.username_input.text,
            'email': self.ids.email_input.text,
            'phone': self.ids.phone_input.text,
            'dob': self.ids.dob_input.text,
            'password': self.ids.password_input.text,
            'confirm_password': self.ids.confirm_password_input.text
        }
        response = requests.post(url, json=data)
        if response.status_code == 201:
            print('User registered successfully')
        else:
            print('Registration failed:', response.json().get('message'))


