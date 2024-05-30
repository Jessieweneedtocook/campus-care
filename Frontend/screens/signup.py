from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
import requests
from Backend.form import (username_checker,
                          password_checker,
                          phone_checker,
                          dob_checker,
                          confirm_password_checker,
                          email_checker)
# Load the KV design file for the SignupScreen
Builder.load_file('kv/signupscreen.kv')
# Define a custom popup class to display errors

'''
Error popup works like in admin.py
'''
class ErrorPopup(Popup):
    def __init__(self, errors, **kwargs):
        super().__init__(**kwargs)
        self.title = "Signup Errors"  # Set the popup title
        self.size_hint = (0.8, 0.5) # Set the size of the popup
        # Create a layout for the popup
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        # Add error messages to the popup
        for error in errors:
            label = Label(text=error, size_hint_y=None, height=dp(30), halign='left', valign='middle')
            label.bind(size=label.setter('text_size'))   # Enable text wrapping for the labels
            layout.add_widget(label)

        # Add a close button to the popup
        close_button = Button(text="Close", size_hint_y=None, height=dp(40))
        close_button.bind(on_release=self.dismiss)
        layout.add_widget(close_button)

        # Add the layout to the popup
        self.add_widget(layout)

# Define the SignupScreen class

'''
-Creates Form for inputting sign up data
-Validates data before sending it to server
-Makes request to server with data and waits for response
-Handles response accordingly
'''
class SignupScreen(Screen):
    # Method to handle user signup
    def sign_up(self):
        # Collect user input data from the screen
        data = {
            'username': self.ids.username.text,
            'email': self.ids.email.text,
            'phone': self.ids.phone.text,
            'DateOfBirth': self.ids.DateOfBirth.text,
            'password': self.ids.password.text,
            'confirm_password': self.ids.confirm_password.text
        }

        # Check if all fields are filled
        if not all(data.values()):
            ErrorPopup(["Please fill in all fields."]).open()
            return

        # Perform validations only if all fields are filled
        validations = [
            username_checker(data["username"]),
            email_checker(data["email"]),
            phone_checker(data["phone"]),
            dob_checker(data["DateOfBirth"]),
            password_checker(data["password"]),
            confirm_password_checker(data["password"], data["confirm_password"])
        ]
        # Collect validation errors
        errors = [message for valid, message in validations if not valid]

        # If there are errors, show them in a popup
        if errors:
            error_popup = ErrorPopup(errors)
            error_popup.open()
            return

        # Prepare the data to send to the backend API
        url = 'http://localhost:5001/api'
        json_data = {"action": "register_user", "role": "user"}
        json_data.update(data)
        # Send a POST request to the API
        response = requests.post(url, json=json_data)
        # Handle the API response
        if response.status_code == 201:
            # If successful, switch to the 'initialoptions' screen
            self.manager.current = 'initialoptions'
            response_json = response.json()
            # Store the access token in the app instance
            App.get_running_app().access_token = response_json.get('access_token')
        else:
            # If there is an error, show the error message in a popup
            error_message = response.json().get('message', 'Registration failed')
            ErrorPopup([error_message]).open()