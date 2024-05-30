from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder
# Load the KV design file for the WellnessHelpScreen
Builder.load_file('kv/wellnesshelpscreen.kv')

# Define the WellnessHelpScreen class, inheriting from Screen
'''
Shows details 
'''
class WellnessHelpScreen(Screen):
    # Method to show details in a popup
    def show_details(self, title, description):
        # Create a Popup with the given title and description
        popup = Popup(title=title, content=Label(text=description), size_hint=(None, None), size=(400, 400))
        # Open the Popup
        popup.open()
