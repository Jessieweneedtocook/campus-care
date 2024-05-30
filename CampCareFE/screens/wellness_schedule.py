import os
import ast
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from datetime import datetime
import calendar
# File path for saving and loading schedule activities
SCHEDULE_FILE = 'schedule_activities.py'
# Load the KV design file for the WellnessScheduleScreen
Builder.load_file('kv/wellnessschedulescreen.kv')
# Define the ActivityPopup class for displaying activities in a popup

'''
Creates calendar for activities
'''

class ActivityPopup(Popup):
    def __init__(self, day_button, screen, **kwargs):
        super().__init__(**kwargs)
        self.day_button = day_button
        self.screen = screen
        self.populate_activities()

    # Method to populate activities in the popup
    '''
    Applies activities to the correct days.
    '''
    def populate_activities(self):
        # Clear existing widgets
        self.ids.logged_activities_box.clear_widgets()
        # Iterate through logged activities and create widgets for each
        for activity in self.day_button.logged_activities:
            box = BoxLayout(orientation='horizontal')
            label = Label(text=activity)
            remove_btn = Button(text="Remove", size_hint_x=None, width=dp(80))
            remove_btn.bind(on_release=lambda btn, act=activity: self.remove_activity(act))
            box.add_widget(label)
            box.add_widget(remove_btn)
            self.ids.logged_activities_box.add_widget(box)

    # Method to remove an activity
    '''
    Removes activity
    '''
    def remove_activity(self, activity):
        # Remove the activity from the logged activities list
        self.day_button.logged_activities.remove(activity)
        self.screen.update_day_button(self.day_button)
        self.populate_activities()
        # Save activities to file
        self.screen.save_activities()
# Define the WellnessScheduleScreen class for managing the wellness schedule screen
class WellnessScheduleScreen(Screen):
    selected_activity = None

    '''
    Generates calendar and loads activities
    '''
    # Method called when the screen is entered
    def on_enter(self):
        self.generate_calendar()
        self.load_activities()

    # Method to generate the calendar layout
    '''
    Creates the calendar for the app
    '''
    def generate_calendar(self):
        calendar_days = self.ids.calendar_days
        calendar_days.clear_widgets()
        # Add labels for days of the week
        days_of_week = ['M', 'T', 'W', 'T', 'F', 'S', 'S']
        for day in days_of_week:
            lbl = Label(text=day, bold=True, color=(1, 1, 1, 1))
            calendar_days.add_widget(lbl)
        # Get the number of days in the current month
        today = datetime.today()
        _, num_days = calendar.monthrange(today.year, today.month)
        # Add buttons for each day of the month
        for day in range(1, num_days + 1):
            btn = Button(text=str(day))
            btn.logged_activities = [] # Initialize logged activities list
            # Bind button press event to handle_day_button_press method
            btn.bind(on_release=lambda btn: self.handle_day_button_press(btn))
            btn.bind(pos=self.update_day_button, size=self.update_day_button)
            calendar_days.add_widget(btn)

    # Method to handle pressing of a day button
    '''
    Shows activities on day when button clicked
    '''
    def handle_day_button_press(self, day_button):
        if self.selected_activity:
            if self.selected_activity not in day_button.logged_activities:
                # Add selected activity to the day's logged activities
                day_button.logged_activities.append(self.selected_activity)
                self.update_day_button(day_button)
                self.save_activities()
        else:
            self.show_activity_popup(day_button)
    # Method to show the activity popup

    '''
    Shows the activities on click
    '''
    def show_activity_popup(self, day_button):
        popup = ActivityPopup(day_button, self)
        popup.open()


    '''
    Updates the day
    '''
    def update_day_button(self, day_button, *args):
        day_button.canvas.after.clear()

        with day_button.canvas.after:
            for idx, activity in enumerate(day_button.logged_activities):
                color = self.get_activity_color(activity)
                Color(*color)  # Set the color
                y_offset = idx * 5
                Rectangle(pos=(day_button.x, day_button.y + y_offset), size=(day_button.width, 10))

    '''
    Applies colour to set activity, defaulting at white
    '''
    def get_activity_color(self, activity):
        colors = {
            'Exercise': (0.1, 0.6, 0.8, 1),
            'Socialisation': (0.816, 0.671, 0.961, 1),
            'Studying': (0.643, 0.851, 0.655, 1),
            'Hobbies': (0.929, 0.659, 0.71, 1),
        }
        return colors.get(activity, (1, 1, 1, 1))  # Default to white if not found
    '''
    Select or deselect activity on button press
    '''
    def select_activity(self, activity, button):
        if self.selected_activity == activity:
            # Deselect the activity if the same button is clicked again
            self.selected_activity = None
            button.background_color = self.get_activity_color(activity)
        else:
            # Reset button colors
            for btn in [self.ids.exercise_btn, self.ids.socialisation_btn, self.ids.studying_btn,
                        self.ids.hobbies_btn]:
                btn.background_color = self.get_activity_color(btn.text)

            self.selected_activity = activity
            button.background_color = [c * 0.5 for c in self.get_activity_color(activity)]

    '''
    Save activities on press
    '''
    def save_activities(self):
        activities = {}
        for day_button in self.ids.calendar_days.children:
            if isinstance(day_button, Button):
                day = day_button.text
                activities[day] = day_button.logged_activities

        with open(SCHEDULE_FILE, 'w') as f:
            f.write('activities = ' + repr(activities) + '\n')

    '''
        Load activities on press
    '''
    def load_activities(self):
        if not os.path.exists(SCHEDULE_FILE):
            return

        with open(SCHEDULE_FILE, 'r') as f:
            content = f.read()
            activities = ast.literal_eval(content.split('= ')[1].strip())

        for day_button in self.ids.calendar_days.children:
            if isinstance(day_button, Button):
                day = day_button.text
                if day in activities:
                    day_button.logged_activities = activities[day]
                    self.update_day_button(day_button)

    '''
    Clears all activities
    '''
    def clear_all_activities(self):
        for day_button in self.ids.calendar_days.children:
            if isinstance(day_button, Button):
                day_button.logged_activities = []
                self.update_day_button(day_button)
        self.save_activities()

    '''
    prints when activity added
    '''
    def add_activity(self):
        print("Add activity button pressed")