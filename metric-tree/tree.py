from .metrics import Metric

class Tree:
    def __init__(self) -> None:
        self.relationships = {}
        self.experiment_group = {}
        self.segment_group = {}

    def add_relationship(self, parent_metric: Metric, child_metric: Metric):
        pass

    def _join_datasets(self):
        pass

    def plot_development(self, parent_metric_name:str, child_metric_name:str):
        pass

    def add_experiment_group(self, experiment_name:str, experiment_groups:dict):
        """This function will add an experiment group to the metric. This way it will be easier to check for differences in the experiment groups.

        This can be used to broadcast all the way through the metric tree to see how each metric is affected.

        Args:
            experiment_name (str): The name of the experiment. This cannot be None.
            experiment_groups (dict): A dictionary which look like the below:
                {
                    "Control": ["userA", "userC"],
                    "Variant1": ["userB", "userD"],
                    "Variant2": ["userE", "userF"],
                    ...
                }
        
        This will make the experiment_group look like this:
        experiment_group = {
            "experiment1": {
                "Control": ["userA", "userC"],
                "Variant1": ["userB", "userD"],
                "Variant2": ["userE", "userF"],
                ...
            },
            "experiment2": ...
        }
        """
        experiment_dict = {
            experiment_name: experiment_groups
        }
        self.experiment_group.update(experiment_dict)

    def add_segment_group(self, segment_name:str, list_of_users:list):
        pass