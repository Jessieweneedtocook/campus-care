import unittest
from CampCareFE.screens.wellness_progress import WellnessProgressScreen
import matplotlib
matplotlib.use('Agg')  # for example, use the 'Agg' backend
import matplotlib.pyplot as plt


class TestWellnessProgressScreen(unittest.TestCase):
    def setUp(self):
        self.screen = WellnessProgressScreen()

    def test_get_last_week_data(self):
        data = self.screen.get_last_week_data()
        self.assertIsInstance(data, list)
        if data:  # if the list is not empty
            self.assertIsInstance(data[0], tuple)

    def test_calculate_stats(self):
        data = [(1, '2024-05-01', 'Running', 'Less than 1'),
                (2, '2024-05-02', 'Swimming', '1-3'),
                (3, '2024-05-03', 'Cycling', 'More than 4')]
        stats = self.screen.calculate_stats(data)
        self.assertEqual(stats, {"Less than 1": 1, "1-3": 1, "More than 4": 1})

        plt.close()  # close the plot window

if __name__ == '__main__':
    unittest.main()
