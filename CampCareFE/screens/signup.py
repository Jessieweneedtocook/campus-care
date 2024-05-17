from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import requests
from kivy.uix.boxlayout import BoxLayout
from users.form import SignupForm
Builder.load_file('kv/signupscreen.kv')


class SignupScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.signup_form = SignupForm()

    def submit_signup_data(self):
        self.signup_form.username.data = self.ids.username_input.text
        self.signup_form.email.data = self.ids.email_input.text
        self.signup_form.phone.data = self.ids.phone_input.text
        self.signup_form.dob.data = self.ids.dob_input.text
        self.signup_form.password.data = self.ids.password_input.text
        self.signup_form.confirm_password.data = self.ids.confirm_password_input.text
        user_data = {
            "username": self.ids.username_input.text,
            "email": self.ids.email_input.text,
            "password": self.ids.password_input.text,
            "confirm_password": self.ids.confirm_password_input.text,
            "dob": self.ids.dob_input.text,
            "number": self.ids.number_input.text
        }
        if self.SignupForm.validate(user_data):
            print('True')
        #    if self.send_to_server(user_data):
        #        print("Success in sending data!")
        #        self.manager.current = 'initialoptions'
        #    else:
        #        print('failed to send data')
        else:
            print('False')
        #    for field, errors in self.signup_form.errors.items():
        #        for error in errors:
        #            print(f"Error in {field}: {error}")

    #def send_to_server(self, user_data):
    #    url = ""
    #    headers = {}
    #    send = requests.post(url, json=user_data)
    #    return send.status_code == 200


