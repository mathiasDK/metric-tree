import unittest
import polars as pl

# Assuming Metric class is defined in metric.py
from ..metrics import Metric

def assert_dataframes_equal(df1, df2):
    # Assert schema equality
    assert df1.schema == df2.schema, "DataFrames have different schemas"

    # Assert data equality
    assert df1.sort(by="*").frame_equal(df2.sort(by="*")) # DataFrames have different data


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


    # Agg func
    def test_validate_agg_function_invalid(self):
        # Define test input data
        data = pl.DataFrame({
            "user_id": [1, 2, 3, 4],
            "period": ["2022-01", "2022-02", "2022-03", "2022-04"],
            "value": [100, 200, 300, 400]
        })
        
        # Assert that a value error is being raised
        with self.assertRaises(ValueError):
            # Create an instance of Metric
            Metric(name="test_metric", data=data, agg_func="my_custom_function")

    def test_validate_agg_function_valid(self):
        # Define test input data
        data = pl.DataFrame({
            "user_id": [1, 2, 3, 4],
            "period": ["2022-01", "2022-02", "2022-03", "2022-04"],
            "value": [100, 200, 300, 400]
        })
        
        # Call the function to be tested
        funcs = ["sum", "mean", "median"]
        for func in funcs:
            try:
                # Create an instance of Metric
                Metric(name="test_metric", data=data, agg_func=func)
            except:
                self.fail("Raised a column error when the data input was valid")

    def test_agg_data_valid(self):
        # Define test input data
        data = pl.DataFrame({
            "user_id": [1, 2, 1, 2],
            "period": ["2022-01", "2022-01", "2022-02", "2022-02"],
            "value": [100, 200, 300, 400],
        })
        metric = Metric(name="test_metric", data=data, agg_func="mean")
        
        output = metric._agg_data(data)
        expected_output = data.groupby(["period"]).agg(pl.mean("value"))

        assert_dataframes_equal(output, expected_output)

    

    def test_agg_data_valid_experiment_columns(self):
        # Define test input data
        data = pl.DataFrame({
            "user_id": [1, 2, 1, 2],
            "period": ["2022-01", "2022-01", "2022-02", "2022-02"],
            "value": [100, 200, 300, 400],
        })
        metric = Metric(name="test_metric", data=data, agg_func="mean")

        data_experiment = pl.DataFrame({
            "user_id": [1, 2, 1, 2],
            "period": ["2022-01", "2022-01", "2022-02", "2022-02"],
            "value": [100, 200, 300, 400],
            "experiment": ["control", "variant", "control", "variant"]
        })
        
        output = metric._agg_data(data_experiment)
        expected_output = data_experiment.groupby(["period", "experiment"]).agg(pl.mean("value"))

        assert_dataframes_equal(output, expected_output)

# If this script is run directly, run the tests
if __name__ == '__main__':
    unittest.main()
