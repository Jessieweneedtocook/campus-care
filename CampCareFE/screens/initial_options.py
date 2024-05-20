from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from CampCareFE.quiz_questions import user_preferences, questions


Builder.load_file('kv/initialoptionsscreen.kv')


class InitialOptionsScreen(Screen):
    def __init__(self, **kwargs):
        super(InitialOptionsScreen, self).__init__(**kwargs)
        self.selected_activities = user_preferences["selected_activities"]

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
        app.save_preferences()



    def insert_preference(self, activity):
        # You need to replace UserID with the actual user ID
        user_id = 1  # Replace this with the actual user ID
        self.cursor.execute("""
                INSERT INTO UserActivityPreferences (UserID, Activity) VALUES (?, ?)""", (user_id, activity))
        self.db_connection.commit()



