import sqlite3

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
        return data

    def calculate_stats(self, data):
        stats = {}
        for row in data:
            activity_type = row[2]
            time_spent_str = row[3]

            # Convert time spent to a numerical value
            if time_spent_str == "Less than 1":
                time_spent = 0.5
            else:
                time_spent = float(time_spent_str)

            if activity_type in stats:
                stats[activity_type] += time_spent
            else:
                stats[activity_type] = time_spent
        print()
        return stats

