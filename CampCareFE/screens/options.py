from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder


Builder.load_file('kv/optionsscreen.kv')


class OptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(OptionsScreen, self).__init__(**kwargs)
        self.selected_activities = []

    def toggle_activity(self, instance):
        if instance.state == 'down':
            instance.background_color = [0.1, 0.5, 0.8, 1]
            if instance.text not in self.selected_activities:
                self.selected_activities.append(instance.text)
        else:
            instance.background_color = [0.8, 0.8, 0.8, 1]
            if instance.text in self.selected_activities:
                self.selected_activities.remove(instance.text)

    def get_selected_activities(self):
        return self.selected_activities

    def on_pre_leave(self):
        from kivy.app import App
        app = App.get_running_app()
        app.selected_activities = self.get_selected_activities()
        app.update_preferences(user_id=1)
