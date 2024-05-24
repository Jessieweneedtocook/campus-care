import requests
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from validationtemp import (
    validate_username, validate_email, validate_phone,
    validate_password, validate_confirm_password
)

class SignupScreen(Screen):
    def submit_signup_data(self):
        # Clear previous error messages
        self.ids.error_message.text = ""

        # Collect user data
        user_data = {
            "username": self.ids.username_input.text,
            "email": self.ids.email_input.text,
            "phone": self.ids.number_input.text,
            "dob": self.ids.dob_input.text,
            "password": self.ids.password_input.text,
            "confirm_password": self.ids.confirm_password_input.text
        }

        # Perform validations
        validations = [
            validate_username(user_data["username"]),
            validate_email(user_data["email"]),
            validate_phone(user_data["phone"]),
            validate_password(user_data["password"]),
            validate_confirm_password(user_data["password"], user_data["confirm_password"])
        ]

        # Check for validation errors
        for valid, message in validations:
            if not valid:
                self.ids.error_message.text = message
                return

        # Send data to server if all validations pass
        if self.send_to_server(user_data):
            print("Success in sending data!")
            self.manager.current = 'initialoptions'
        else:
            self.ids.error_message.text = 'Failed to send data'

    def send_to_server(self, user_data):
        url = "https://yourapiendpoint.com/signup"
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(url, json=user_data, headers=headers)
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Error sending data to server: {e}")
            return False