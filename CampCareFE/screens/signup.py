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
        if self.send_to_server(user_data):
            print("Success in sending data!")
            self.manager.current = 'initialoptions'
        else:
            print('failed to send data')

    def send_to_server(self, user_data):
        url = ""
        headers = {}
        send = requests.post(url, json=user_data)
        return send.status_code == 200

