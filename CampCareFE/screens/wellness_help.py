from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.lang import Builder

Builder.load_file('kv/wellnesshelpscreen.kv')

'''
Shows details 
'''
class WellnessHelpScreen(Screen):
    def show_details(self, title, description):
        popup = Popup(title=title, content=Label(text=description), size_hint=(None, None), size=(400, 400))
        popup.open()
