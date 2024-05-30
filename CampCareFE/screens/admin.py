from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
import requests

Builder.load_file('kv/adminscreen.kv')


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


class DeleteAccountPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Delete User"
        self.size_hint = (0.8, 0.8)
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))

        # Get list of users
        url = 'http://localhost:5001/api'
        token = App.get_running_app().access_token
        headers = {'Authorization': f'Bearer {token}'}
        data = {
            "action": "view_users",
        }
        response = requests.post(url, headers=headers, json=data)
        data = response.json()
        users = data.get("usernames")

        # Add a scrollable list of users
        user_list = GridLayout(cols=1, size_hint_y=None)
        user_list.bind(minimum_height=user_list.setter('height'))

        for user in users:
            user_list.add_widget(Label(text=user, size_hint_y=None, height=dp(40)))

        scroll_view = ScrollView(size_hint=(1, None), size=(dp(400), dp(200)))
        scroll_view.add_widget(user_list)

        layout.add_widget(scroll_view)

        # Add a text input for entering the username to delete
        self.user_to_delete_input = TextInput(hint_text='Enter username to delete', multiline=False, size_hint_y=None,
                                              height=dp(40))
        layout.add_widget(self.user_to_delete_input)

        # Add a button to delete the user
        delete_button = Button(text='Delete', size_hint_y=None, height=dp(40))
        delete_button.bind(on_release=self.delete_user)
        layout.add_widget(delete_button)

        self.add_widget(layout)

    def delete_user(self, instance):
        username_to_delete = self.user_to_delete_input.text
        url = 'http://localhost:5001/api'
        token = App.get_running_app().access_token
        headers = {'Authorization': f'Bearer {token}'}
        json_data = {"action": "admin_delete_account", 'delete_username': username_to_delete}
        print("Data to be sent ", headers, json_data)
        try:
            response = requests.post(url, headers=headers, json=json_data)

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


class AdminScreen(Screen):
    def show_delete_account(self):
        DeleteAccountPopup().open()
