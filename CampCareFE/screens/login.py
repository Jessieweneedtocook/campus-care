from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
import requests

Builder.load_file('kv/loginscreen.kv')

class ErrorPopup(Popup):
    def __init__(self, errors, **kwargs):
        super().__init__(**kwargs)
        self.title = "Login Errors"
        self.size_hint = (0.8, 0.5)

        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        for error in errors:
            label = Label(text=error, size_hint_y=None, height=dp(30), halign='left', valign='middle')
            label.bind(size=label.setter('text_size'))  # Enable text wrapping
            layout.add_widget(label)

        close_button = Button(text="Close", size_hint_y=None, height=dp(40))
        close_button.bind(on_release=self.dismiss)
        layout.add_widget(close_button)

        self.add_widget(layout)

class LoginScreen(Screen):
    def login(self):
        self.ids.error_message.text = ""
        username = self.ids.username.text
        password = self.ids.password.text

        # Ensure both fields are filled
        if not username or not password:
            ErrorPopup(["Please fill in all fields."]).open()
            return

        # Send login request to the backend
        url = 'http://localhost:5001/api'
        response = requests.post(url, json={"action": "login_user", "username": username, "password": password})
        try:
            response_json = response.json()
        except requests.exceptions.JSONDecodeError:
            ErrorPopup(["Server error"]).open()
            return

        if response.status_code == 200:
            response_json = response.json()
            App.get_running_app().access_token = response_json.get('access_token')
            self.manager.current = 'home'
        else:
            error_message = response_json.get('message', 'Login failed')
            ErrorPopup([error_message]).open()
