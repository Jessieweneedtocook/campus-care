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
    def sign_up(self):
        self.ids.error_message.text = ""
        data = {
            'username': self.ids.username_input.text,
            'email': self.ids.email_input.text,
            'phone': self.ids.phone_input.text,
            'dob': self.ids.dob_input.text,
            'password': self.ids.password_input.text,
            'confirm_password': self.ids.confirm_password_input.text
        }

        validations = [
            username_checker(data["username"]),
            email_checker(data["email"]),
            phone_checker(data["phone"]),
            dob_checker(data["dob"]),
            password_checker(data["password"]),
            confirm_password_checker(data["password"], data["confirm_password"])
           ]

        for valid, message in validations:
            if not valid:
                self.ids.error_message.text = message
                return

        if self.send_to_server(data):
            print("Success in sending data!")
            self.manager.current = 'initialoptions'
        else:
            self.ids.error_message.text = 'Failed to send data'

    def send_to_server(self, user_data):
        url = "http://127.0.0.1:5000"
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, json=user_data, headers=headers)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to server: {e}")
            return False


