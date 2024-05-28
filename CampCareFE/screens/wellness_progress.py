import sqlite3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from kivy.properties import StringProperty

from math import pi
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from CampCareFE.screens.daily_quiz import db_path

Builder.load_file('kv/wellnessprogressscreen.kv')

class WellnessProgressScreen(Screen):

    needs_improvement_output = StringProperty('')
    most_improved_output = StringProperty('')

    def on_enter(self):
        self.update_most_improved_text()
        self.update_needs_improvement_text()

    def get_data_for_period(self, days):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Get activities for the past 'days' days
        cursor.execute(f"""
                    SELECT * FROM UserActivities
                    WHERE ActivityDate >= date('now', '-{days} days')
                        AND ActivityDate < date('now')
                """)

        data = cursor.fetchall()
        conn.close()

        return self.data_by_activity_type(data)

    def data_by_activity_type(self, data):
        # Initialize an empty dictionary to store the data
        data_by_activity_type = {}
        # Loop through the data
        for row in data:
            # Assume the activity type is in the third column
            activity_type = row[1]

            # If this activity type is not in the dictionary yet, add it
            if activity_type not in data_by_activity_type:
                data_by_activity_type[activity_type] = []

            # Add this row of data to the appropriate list in the dictionary
            data_by_activity_type[activity_type].append(row)

        return data_by_activity_type

    def calculate_stats(self, data_by_activity_type):
        stats_by_activity_type = {}

        for activity_type, data in data_by_activity_type.items():
            total_value = 0
            count = len(data)

            # Convert each time spent string to its corresponding numerical value
            for row in data:
                time_spent_str = row[2]  # Assuming time_spent is the third column
                if time_spent_str == "Less than 1":
                    total_value += 0
                elif time_spent_str == "1-3":
                    total_value += 2
                elif time_spent_str == "More than 4":
                    total_value += 5
                elif time_spent_str == "Less than 5":
                    total_value += 4
                elif time_spent_str == "5-7":
                    total_value += 6
                elif time_spent_str == "More than 7":
                    total_value += 8

            # Calculate the average
            average_value = total_value / count if count > 0 else 0
            stats_by_activity_type[activity_type] = average_value

        return stats_by_activity_type

    def plot_stats(self, stats_by_activity_type):
        # Define the labels of your chart
        labels = np.array(list(stats_by_activity_type.keys()))
        num_vars = len(labels)

        # Add data
        data = np.array(list(stats_by_activity_type.values()))

        # Compute angle of each axis
        angles = np.linspace(0, 2 * pi, num_vars, endpoint=False).tolist()

        # Make the plot close on itself
        data = np.concatenate((data, [data[0]]))
        angles += angles[:1]

        # Create figure and polar projection
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))

        # Draw one axe per variable and add labels
        plt.xticks(angles[:-1], labels, color='grey', size=12)

        # Draw ylabels
        ax.set_rlabel_position(30)
        plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], color="grey", size=7)
        plt.ylim(0, 5)

        # Plot data
        ax.plot(angles, data, linewidth=1, linestyle='solid', label="Activity Average")

        # Fill area
        ax.fill(angles, data, 'b', alpha=0.1)

        plt.savefig('assets/output.png')

    def get_last_week(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT * FROM UserActivities
            WHERE ActivityDate >= date('now', '-7 days')
                AND ActivityDate < date('now')
        """)

        data = cursor.fetchall()
        conn.close()
        return data

    def get_week_before(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(f"""
            SELECT * FROM UserActivities
            WHERE ActivityDate >= date('now', '-14 days')
                AND ActivityDate < date('now', '-7 days')
        """)

        data = cursor.fetchall()
        conn.close()
        return data

    def most_improved(self):
        data_past_week = self.data_by_activity_type(self.get_last_week())
        data_week_before = self.data_by_activity_type(self.get_week_before())

        current_stats = self.calculate_stats(data_past_week)
        prev_stats = self.calculate_stats(data_week_before)

        most_improved = max(current_stats, key=lambda x: current_stats[x] - prev_stats.get(x, 0) if x != 'Drinking' else prev_stats.get(x, 0) - current_stats[x])
        return most_improved

    def needs_improvement(self):
        data_past_week = self.data_by_activity_type(self.get_last_week())
        data_week_before = self.data_by_activity_type(self.get_week_before())

        current_stats = self.calculate_stats(data_past_week)
        prev_stats = self.calculate_stats(data_week_before)

        needs_improvement = min(current_stats, key=lambda x: current_stats[x] - prev_stats.get(x, 0) if x != 'Drinking' else prev_stats.get(x, 0) - current_stats[x])
        return needs_improvement

    def overall_progress(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(f"""
                    SELECT * FROM UserActivities
                """)

        data = cursor.fetchall()
        conn.close()

        stats_by_activity_type = self.calculate_stats(self.data_by_activity_type(data))
        # Create a figure and a set of subplots
        fig, ax = plt.subplots()

        # Plot the data
        activities = list(stats_by_activity_type.keys())
        times = list(stats_by_activity_type.values())
        y_pos = np.arange(len(activities))

        ax.barh(y_pos, times, align='center')
        ax.set_yticks(y_pos)
        ax.set_yticklabels(activities, fontsize=10)  # Increase font size
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Time Spent (Hours)', fontsize=12)  # Increase font size
        ax.set_title('Overall Progress', fontsize=14)  # Increase font size

        plt.tight_layout()  # Adjust layout to fit labels
        plt.savefig('assets/overall_progress.png')




    def update_needs_improvement_text(self):
        needs_improvement_activity = self.needs_improvement()
        if needs_improvement_activity:
            self.needs_improvement_output = f"Needs Improvement:\n- {needs_improvement_activity}"
        else:
            self.needs_improvement_output = "Needs Improvement:\n- No data from previous week"

    def update_most_improved_text(self):
        most_improved_activity = self.most_improved()

        if most_improved_activity:
            self.most_improved_output = f"Most Improved:\n- {most_improved_activity}"

        else:
            self.most_improved_output = "Most Improved:\n- No data from previous week"

from kivy.uix.button import Button
import webbrowser
class ShareTwitter(Button):
    def on_release(self):
        screen = self.get_screen()  # Find the screen that this button is part of
        text = f'{screen.most_improved_output}\n{screen.needs_improvement_output}'

        # The URL for sharing on Twitter
        share_url = f'https://twitter.com/intent/tweet?text={text}'

        webbrowser.open(share_url)

    def get_screen(self):
        # Traverse up the widget tree to find the WellnessProgressScreen
        parent = self.parent
        while parent:
            if isinstance(parent, WellnessProgressScreen):
                return parent
            parent = parent.parent
        return None

class ShareFacebook(Button):
    def on_release(self):
        screen = self.get_screen()  # Find the screen that this button is part of
        text = f'{screen.most_improved_output}\n{screen.needs_improvement_output}'

        share_url = f'https://www.facebook.com/sharer/sharer.php?text={text}'

        webbrowser.open(share_url)

    def get_screen(self):
        # Traverse up the widget tree to find the WellnessProgressScreen
        parent = self.parent
        while parent:
            if isinstance(parent, WellnessProgressScreen):
                return parent
            parent = parent.parent
        return None