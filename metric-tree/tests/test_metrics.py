import unittest
import polars as pl

# Assuming Metric class is defined in metric.py
from ..metrics import Metric

class TestMetric(unittest.TestCase):
    def test_validate_data_input_valid_columns(self):
        # Define test input data
        data = pl.DataFrame({
            "user_id": [1, 2, 3, 4],
            "period": ["2022-01", "2022-02", "2022-03", "2022-04"],
            "value": [100, 200, 300, 400]
        })
        
        # Create an instance of Metric
        metric = Metric(name="test_metric", data=data)
        
        # Call the function to be tested
        try:
            metric._Metric__validate_data_input()
        except:
            self.fail("Raised a column error when the data input was valid")

    def test_validate_data_input_invalid_columns_names(self):
        # Define test input data
        data = pl.DataFrame({
            "id": [1, 2, 3, 4],
            "period": ["2022-01", "2022-02", "2022-03", "2022-04"],
            "value": [100, 200, 300, 400]
        })
        
        # Create an instance of Metric
        metric = Metric(name="test_metric", data=data)

        with self.assertRaises(ValueError):
            metric._Metric__validate_data_input()
        
        # Assert that a value error is being raised
        # self.assertRaises(ValueError, metric._Metric__validate_data_input())

    def test_validate_data_input_invalid_columns_number(self):
        # Define test input data
        data = pl.DataFrame({
            "user_id": [1, 2, 3, 4],
            "period": ["2022-01", "2022-02", "2022-03", "2022-04"],
            "value": [100, 200, 300, 400],
            "extra_column": [1,2,3,4],
        })
        
        # Create an instance of Metric
        metric = Metric(name="test_metric", data=data)
        
        # Assert that a value error is being raised
        with self.assertRaises(ValueError):
            metric._Metric__validate_data_input()


# If this script is run directly, run the tests
if __name__ == '__main__':
    unittest.main()
