from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
import requests
# import validation functions

Builder.load_file('kv/signupscreen.kv')


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
            #username_validation(user_data["username"]),
            #email_validation(user_data["email"]),
            #phone_validation(user_data["phone"]),
            #password_validation(user_data["password"]),
            #confirm_password_validation(user_data["password"], user_data["confirm_password"])
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
