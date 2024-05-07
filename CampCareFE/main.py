from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window


# Define the Login Screen
class LoginScreen(Screen):
    pass


# Main Application Class
class CampusCareApp(App):
    def build(self):
        Window.size = (375, 812)  # Use (width, height) in pixels

        # Optionally, you can set the position and disable resizing
        Window.top = 100
        Window.left = 100
        Window.borderless = False  # Set to True for borderless window
        Window.resizable = False  # Prevent resizing to mimic app behavior
        Builder.load_file('kv/loginscreen.kv')

        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        return sm


if __name__ == '__main__':
    CampusCareApp().run()