import polars as pl

class Metric:
    def __init__(self, name:str, data: pl.DataFrame)->None:
        self.name = name
        self.data = data
        self.experiment_group = {}
        self.segment_group = {}

        # Validating input
        self.__validate_input()

    def __validate_input(self):
        self.__validate_data_input()
    
    def __validate_data_input(self):
        _valid_column_names = ["user_id", "period", "value"]
        cols = self.data.columns
        
        for col in cols:
            if col not in _valid_column_names:
                raise ValueError(f"Please provide valid column names which should be: {_valid_column_names}")
            
        for col in _valid_column_names:
            if col not in cols:
                raise ValueError(f"Please provide all three columns: {_valid_column_names}")

    def add_experiment_group(self, experiment_name:str, experiment_lookup:dict):
        pass

    def add_segment_group(self, segment_name:str, list_of_users:list):
        pass

    def plot_development():
        pass