import polars as pl

class Metric:
    def __init__(self, name:str, data: pl.DataFrame)->None:
        self.name = name
        self.data = data

    def add_experiment_group(self, experiment_name:str, experiment_lookup:dict):
        pass

    def add_segment_group(self, segment_name:str, list_of_users:list):
        pass

    def plot_development():
        pass