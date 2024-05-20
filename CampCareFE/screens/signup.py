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
            'username': self.ids.username.text,
            'email': self.ids.email.text,
            'phone': self.ids.number.text,
            'dob': self.ids.dob.text,
            'password': self.ids.password.text,
            'confirm_password': self.ids.confirm_password.text
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
                print('error message')
                self.ids.error_message.text = message
                return



        #url = 'http://localhost:5000/register'

        #response = requests.post(url, json=data)
        #if response.status_code == 201:
        #    print('User registered successfully')
        #else:
        #    print('Registration failed:', response.json().get('message'))



