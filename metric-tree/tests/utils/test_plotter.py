from ...utils.plotter import Plotter

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import unittest
from unittest.mock import Mock


class TestLinePlot(unittest.TestCase):
    def setUp(self):
        # Create an instance of YourClass for testing
        self.instance = Plotter()

        # Define some mock dataframes for testing
        self.df1 = pd.DataFrame({
            'x': [1, 2, 1, 2],
            'y': [10, 20, 30, 40],
            'color': ['A', 'A', 'B', 'B']
        })

        self.df2 = pd.DataFrame({
            'x': [1, 2, 1, 2],
            'y': [10, 20, 30, 40],
            'color': ['Control', 'Control', 'Variant', 'Variant']
        })

    def test_line_plot_default(self):
        # Test line_plot with default arguments
        fig = self.instance.line_plot(self.df1, 'x', 'y')
        self.assertIsInstance(fig, go.Figure)

    def test_line_plot_experiment_comparison(self):
        # Test line_plot with experiment_comparison=True
        fig = self.instance.line_plot(self.df2, 'x', 'y', experiment_comparison=True, color="color")
        self.assertIsInstance(fig, go.Figure)

    def test_line_plot_with_color(self):
        # Test line_plot with a specified color column
        fig = self.instance.line_plot(self.df1, 'x', 'y', color='color')
        self.assertIsInstance(fig, go.Figure)

    def test_line_plot_color_dict(self):
        # Test whether the color dictionary is correctly generated
        variant_color = self.instance.colorway[0]
        control_color = self.instance.secondary_colors["light_grey"]
        
        # Mocking the '_set_end_label' method to prevent errors
        # self.instance._set_end_label = Mock(return_value=None)

        # Call the line_plot method with experiment_comparison=True
        fig = self.instance.line_plot(self.df2, 'x', 'y', experiment_comparison=True, color="color")

        actual_color_dict = {}
        for d in fig.data:
            if d.mode == "lines":
                actual_color_dict[d.name] = d.line.color
        
        # Check if the color dictionary is generated correctly
        expected_color_dict = {'Control': control_color, 'Variant': variant_color,}
        self.assertDictEqual(actual_color_dict, expected_color_dict)

    def test_line_plot_end_labels(self):
        # Test whether end labels are added correctly
        self.instance._set_end_label = Mock(return_value=None)

        # Call the line_plot method
        fig = self.instance.line_plot(self.df1, 'x', 'y', color="color")
        
        # Check if the _set_end_label method was called for each data point
        self.assertEqual(self.instance._set_end_label.call_count, len(self.df1["color"].unique()))

if __name__ == '__main__':
    unittest.main()
