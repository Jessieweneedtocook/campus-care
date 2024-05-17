import sqlite3
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from math import pi
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from CampCareFE.screens.daily_quiz import db_path

Builder.load_file('kv/wellnessprogressscreen.kv')

class WellnessProgressScreen(Screen):
    def get_last_week_data(self):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM UserActivities
            WHERE ActivityDate >= date('now','-7 days')
        """)

        data = cursor.fetchall()
        conn.close()

        # Initialize an empty dictionary to store the data
        data_by_activity_type = {}

        # Loop through the data
        for row in data:
            # Assume the activity type is in the third column
            activity_type = row[2]

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
                time_spent_str = row[3]
                if time_spent_str == "Less than 1":
                    total_value += 0
                elif time_spent_str == "1-3":
                    total_value += 2
                elif time_spent_str == "More than 4":
                    total_value += 5

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

