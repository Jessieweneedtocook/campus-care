from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.metrics import dp
import requests
from kivy.app import App

Builder.load_file('kv/userinfoscreen.kv')

class ErrorPopup(Popup):
    def __init__(self, errors, **kwargs):
        super().__init__(**kwargs)
        self.title = "Error"
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

class SuccessPopup(Popup):
    def __init__(self, message, **kwargs):
        super().__init__(**kwargs)
        self.title = "Success"
        self.size_hint = (0.8, 0.5)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        label = Label(text=message, size_hint_y=None, height=dp(30), halign='left', valign='middle')
        label.bind(size=label.setter('text_size'))  # Enable text wrapping
        layout.add_widget(label)

        close_button = Button(text="Close", size_hint_y=None, height=dp(40))
        close_button.bind(on_release=self.dismiss)
        layout.add_widget(close_button)

        self.add_widget(layout)

class ChangeEmailPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Change Email"
        self.size_hint = (0.8, 0.5)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        self.new_email_input = TextInput(hint_text="New Email", multiline=False, size_hint_y=None, height=dp(40))
        layout.add_widget(self.new_email_input)

        submit_button = Button(text="Submit", size_hint_y=None, height=dp(40))
        submit_button.bind(on_release=self.change_email)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def change_email(self, instance):
        new_email = self.new_email_input.text
        if not new_email:
            ErrorPopup(["Please provide a new email address."]).open()
            return

        url = 'http://localhost:5001/api'
        token = App.get_running_app().access_token
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, json={"action": "change_email", "new_email": new_email}, headers=headers)

        if response.status_code == 200:
            SuccessPopup("Email updated successfully.").open()
        else:
            error_message = response.json().get('message', 'Error updating email')
            ErrorPopup([error_message]).open()
        self.dismiss()

class ChangePasswordPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Change Password"
        self.size_hint = (0.8, 0.5)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        self.current_password_input = TextInput(hint_text="Current Password", multiline=False, password=True, size_hint_y=None, height=dp(40))
        layout.add_widget(self.current_password_input)

        self.new_password_input = TextInput(hint_text="New Password", multiline=False, password=True, size_hint_y=None, height=dp(40))
        layout.add_widget(self.new_password_input)

        self.confirm_new_password_input = TextInput(hint_text="Confirm New Password", multiline=False, password=True, size_hint_y=None, height=dp(40))
        layout.add_widget(self.confirm_new_password_input)

        submit_button = Button(text="Submit", size_hint_y=None, height=dp(40))
        submit_button.bind(on_release=self.change_password)
        layout.add_widget(submit_button)

        self.add_widget(layout)

    def change_password(self, instance):
        current_password = self.current_password_input.text
        new_password = self.new_password_input.text
        confirm_new_password = self.confirm_new_password_input.text

        if not all([current_password, new_password, confirm_new_password]):
            ErrorPopup(["Please fill in all fields."]).open()
            return

        url = 'http://localhost:5001/api'
        token = App.get_running_app().access_token
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, json={"action": "change_password", "current_password": current_password, "new_password": new_password, "confirm_new_password": confirm_new_password}, headers=headers)

        if response.status_code == 200:
            SuccessPopup("Password updated successfully.").open()
        else:
            error_message = response.json().get('message', 'Error updating password')
            ErrorPopup([error_message]).open()
        self.dismiss()


class ConfirmDeletePopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Confirm Delete"
        self.size_hint = (0.8, 0.5)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        label = Label(text="Are you sure you want to delete your account?", size_hint_y=None, height=dp(40))
        layout.add_widget(label)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        yes_button = Button(text="Yes")
        yes_button.bind(on_release=self.delete_user)
        no_button = Button(text="No")
        no_button.bind(on_release=self.dismiss)
        button_layout.add_widget(yes_button)
        button_layout.add_widget(no_button)
        layout.add_widget(button_layout)

        self.add_widget(layout)

    def delete_user(self, instance):
        url = 'http://localhost:5001/api'
        token = App.get_running_app().access_token
        headers = {'Authorization': f'Bearer {token}'}
        json_data = {"action": "delete_account"}

        try:
            response = requests.delete(url, headers=headers, json=json_data)

            try:
                response_json = response.json()
            except requests.exceptions.JSONDecodeError:
                error_message = "Error deleting account"
                ErrorPopup([error_message]).open()
                self.dismiss()
                return

            if response.status_code == 200:
                SuccessPopup("Account deleted successfully.").open()
                App.get_running_app().logout()
            else:
                error_message = response_json.get('message', 'Error deleting account')
                ErrorPopup([error_message]).open()

        except Exception as e:
            ErrorPopup([str(e)]).open()

        self.dismiss()

class UserInfoScreen(Screen):
    def show_change_email(self):
        ChangeEmailPopup().open()

    def show_change_password(self):
        ChangePasswordPopup().open()

    def show_confirm_delete(self):
        ConfirmDeletePopup().open()

    def logout(self):
        url = 'http://localhost:5001/api'
        token = App.get_running_app().access_token
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, json={"action": "logout"}, headers=headers)

        if response.status_code == 200:
            App.get_running_app().logout()
        else:
            error_message = response.json().get('message', 'Error logging out')
            ErrorPopup([error_message]).open()