from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import requests
from kivy.app import App

Builder.load_file('kv/loginscreen.kv')


class LoginScreen(Screen):
    def login(self):
        self.ids.error_message.text = ""
        username = self.ids.username.text
        password = self.ids.password.text

        # Ensure both fields are filled
        if not username or not password:
            self.ids.error_message.text = "Please fill in all fields"
            return

        # Send login request to the backend
        url = 'http://localhost:5001/api'
        response = requests.post(url, json={"action": "login_user", "username": username, "password": password})

        if response.status_code == 200:
            self.manager.current = 'home'
        else:
            self.ids.error_message.text = response.json().get('message')
