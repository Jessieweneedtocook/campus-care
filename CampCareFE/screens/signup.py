from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import requests

Builder.load_file('kv/signupscreen.kv')


class SignupScreen(Screen):
    def submit_signup_data(self):
        user_data = {
            "username": self.ids.username_input.text,
            "email": self.ids.email_input.text,
            "password": self.ids.password_input.text,
            "confirm_password": self.ids.confirm_password_input.text,
            "dob": self.ids.dob_input.text,
            "number": self.ids.number_input.text
        }
        # authentication here
        self.send_to_server(user_data)

    def send_to_server(self, user_data):
        url = ""
        headers = {}
        send = requests.post(url, json=user_data)
        if send.status_code == 200:
            print("Signup successful!")

        else:
            print("Failed to sign up. Status code:", send.status_code)


