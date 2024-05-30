from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# aboutscreen.kv loaded by builder when about selected in user info
Builder.load_file('kv/aboutscreen.kv')

'''
About class defined here
'''
class AboutScreen(Screen):

    pass

