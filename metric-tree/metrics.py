import polars as pl
from .utils.plotter import Plotter

class Metric:
    def __init__(self, name:str, data: pl.DataFrame, agg_func:str)->None:
        self.name = self.__validate_name(name)
        self.data = self.__validate_data_input(data)
        self.agg_func = self.__validate_agg_func(agg_func)

    def __validate_name(self, name):
        if name is None:
            raise ValueError("Please provide an actual name for the metric")
        
        return name
    
    def __validate_data_input(self, data):
        _valid_column_names = ["user_id", "period", "value"]
        cols = data.columns
        
        for col in cols:
            if col not in _valid_column_names:
                raise ValueError(f"Please provide valid column names which should be: {_valid_column_names}")
            
        for col in _valid_column_names:
            if col not in cols:
                raise ValueError(f"Please provide all three columns: {_valid_column_names}")
            
        return data
    
    def __validate_agg_func(self, agg_func):
        _valid_agg_funcs = ["sum", "mean", "median"]
        if agg_func in _valid_agg_funcs:
            self.agg_func = agg_func
        else:
            raise ValueError(f"Please provide a valid aggregate function {_valid_agg_funcs}")
        return agg_func
    
    def _agg_data(self, data)->pl.DataFrame:
        # drop the user id column, but keep all others.
        data = data.drop("user_id")
        value_col = "value"
        grouping_cols = [col for col in data.columns if col!=value_col]
        if self.agg_func == "sum":
            data = data.groupby(grouping_cols).agg(pl.sum(value_col))
        elif self.agg_func == "mean":
            data = data.groupby(grouping_cols).agg(pl.mean(value_col))
        elif self.agg_func == "median":
            data = data.groupby(grouping_cols).agg(pl.median(value_col))
        else:
            raise ValueError("Please provide a valid aggregate function.")
        
        return data

    def plot_development(self):
        p = Plotter()
        plot_data = self._agg_data(self.data)
        fig = p.line_plot(plot_data, x="period", y="value")
        return fig
    
    def plot_development_by_experiment(self, experiment_name:str):
        p = Plotter()
        data = self.data # Add experiments
        plot_data = self._agg_data(data)
        fig = p.line_plot_experiment(plot_data, x="period", y="value", color="variant_group")
        return fig
    
    def plot_development_by_segments(self, segments:list):
        p = Plotter()
        data = self.data # Add segments
        plot_data = self._agg_data(data)
        fig = p.line_plot(plot_data, x="period", y="value", color="segment")
        return fig


if __name__ == "__main__":
    data = pl.DataFrame({
            "id": [1, 2, 3, 4],
            "period": ["2022-01", "2022-02", "2022-03", "2022-04"],
            "value": [100, 200, 300, 400]
        })
    metric = Metric(name="test", data=data)
    metric._Metric__validate_data_input()
    metric.add_experiment_group()