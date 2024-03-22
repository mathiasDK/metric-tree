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
        
        # Call the function to be tested
        try:
            # Create an instance of Metric
            Metric(name="test_metric", data=data, agg_func="mean")
        except:
            self.fail("Raised a column error when the data input was valid")

    def test_validate_data_input_invalid_columns_names(self):
        # Define test input data
        data = pl.DataFrame({
            "id": [1, 2, 3, 4],
            "period": ["2022-01", "2022-02", "2022-03", "2022-04"],
            "value": [100, 200, 300, 400]
        })        

        with self.assertRaises(ValueError):
            # Create an instance of Metric
            Metric(name="test_metric", data=data, agg_func="mean")

    def test_validate_data_input_invalid_columns_number(self):
        # Define test input data
        data = pl.DataFrame({
            "user_id": [1, 2, 3, 4],
            "period": ["2022-01", "2022-02", "2022-03", "2022-04"],
            "value": [100, 200, 300, 400],
            "extra_column": [1,2,3,4],
        })
        
        # Assert that a value error is being raised
        with self.assertRaises(ValueError):
            # Create an instance of Metric
            Metric(name="test_metric", data=data, agg_func="mean")


# If this script is run directly, run the tests
if __name__ == '__main__':
    unittest.main()
