import numpy as np
import polars as pl
from datetime import datetime, timedelta

np.random.seed(42) # Ensuring similar datasets

class SimulateData:
    def __init__(self, n_metrics:int, n_periods:int, n_users:int) -> None:
        """This class can be used to generate a fictive dataset which can be used to showcase and test the rest of the packages.
        The main function is the _create_dataset() which creates a dataset that contains n_metrics, n_users over n_periods.

        It will also be possible to add experiments and segments as well.

        Args:
            n_metrics (int): The number of metrics which should be included in the data.
            n_periods (int): The number of periods which should be included. This will be the number of weeks up to today.
            n_users (int): The number of users in the data.
        """
        self.n_metrics = n_metrics
        self.n_periods = n_periods
        self.n_users = n_users
        self.experiment_groups = {}
        self.segments = {}
        self._create_dataset()

    def _create_dataset(self) -> pl.DataFrame:
        """This function will create a dataset which looks like the below:
        ┌───────────┬────────────┬───────────┬─────────┬─────────────────────┐
        │ metric_0  ┆ metric_1   ┆ metric_2  ┆ user_id ┆ period              │
        │ ---       ┆ ---        ┆ ---       ┆ ---     ┆ ---                 │
        │ f64       ┆ f64        ┆ f64       ┆ i64     ┆ datetime[μs]        │
        ╞═══════════╪════════════╪═══════════╪═════════╪═════════════════════╡
        │ 43.908562 ┆ 94.924891  ┆ 76.017345 ┆ 1       ┆ 2024-01-15 00:00:00 │
        │ 43.840674 ┆ 95.834441  ┆ 77.031065 ┆ 2       ┆ 2024-01-15 00:00:00 │
        │ 42.971133 ┆ 95.039353  ┆ 74.755778 ┆ 3       ┆ 2024-01-15 00:00:00 │
        │ 43.845312 ┆ 95.074065  ┆ 75.029208 ┆ 4       ┆ 2024-01-15 00:00:00 │
        │ 43.790298 ┆ 95.179498  ┆ 74.796139 ┆ 5       ┆ 2024-01-15 00:00:00 │
        │ …         ┆ …          ┆ …         ┆ …       ┆ …                   │
        │ 49.103059 ┆ 105.149082 ┆ 83.969945 ┆ 1       ┆ 2024-03-18 00:00:00 │
        │ 46.530453 ┆ 103.032383 ┆ 81.218897 ┆ 2       ┆ 2024-03-18 00:00:00 │
        │ 48.409177 ┆ 105.269834 ┆ 84.696498 ┆ 3       ┆ 2024-03-18 00:00:00 │
        │ 46.470737 ┆ 102.98987  ┆ 79.523868 ┆ 4       ┆ 2024-03-18 00:00:00 │
        │ 48.282965 ┆ 103.449336 ┆ 84.496887 ┆ 5       ┆ 2024-03-18 00:00:00 │
        └───────────┴────────────┴───────────┴─────────┴─────────────────────┘

        Each metric will naturally increase over time to look like it is trending. 
        Each metrics will also have some covariance with the other metrics to ensure that the developments per users aren't completely at random.   

        Returns:
            pl.DataFrame: The dataframe which can be seen above.
        """

        # Creating the base data with some covariance
        metric_means = np.random.uniform(10, 100, size=self.n_metrics)
        metric_cov_base = np.random.rand(self.n_metrics, self.n_metrics)
        metric_cov = np.dot(metric_cov_base, metric_cov_base.transpose())
        data = np.random.multivariate_normal(metric_means, metric_cov, (self.n_users, self.n_periods)) # shape(n_users, n_periods, n_metrics)

        # List of user ids and periods
        user_ids = np.linspace(1, self.n_users, self.n_users).astype(int)
        periods = np.arange(datetime(1985,7,1), datetime.now(), timedelta(weeks=1)).astype(datetime)
        periods = periods[len(periods)-self.n_periods:]

        # Creating the trend
        first_timestamp = min(periods).timestamp()
        period_trend = np.array([p.timestamp()/first_timestamp for p in periods]) * np.random.normal(0.005, 0.01, size=self.n_periods) + 1 # increase over time
        period_trend = np.cumprod(period_trend) # Doing a cumulative sum to ensure trend

        # Multiplying the trend to the existing data
        for i, period_value in enumerate(period_trend):
            data[:, i, :] *= period_value

        # Adding to polars dataframe
        metric_cols = [f"metric_{i}" for i in range(self.n_metrics)]
        dfs = []
        for i, period in enumerate(periods):
            sub_data = data[:, i, :].T.reshape((self.n_metrics, self.n_users))
            df = pl.from_numpy(data=sub_data, schema=metric_cols)
            df = (
                df
                .with_columns(
                    pl.Series(name="user_id", values=user_ids),
                    pl.Series(name="period", values=[period]*self.n_users),
                )
            )
            dfs.append(df)
        data = pl.concat(dfs)
        self.data = data

    def add_experiment(self, experiment_name:str, experiment_start_date:datetime, experiment_groups:dict):
        """Creating experiment groups and altering the metrics slightly after the experiment went live for the non control groups.
        Do note that one of the experiment groups should be named 'control' - otherwise they will all be considered variant groups.

        Args:
            experiment_name (str): The name of the experiment.
            experiment_start_date (datetime): The date the experiment went live, which is the date the data will be altered from.
            experiment_groups (dict): A dictionary of each group and the users in each group. It should look like this:
                {
                    "control": [1,2,3,4],
                    "variant": [5,6,7,8],
                    "variant2": etc.
                } 
        """
        variant_users = []
        for group, users in experiment_groups.items():
            if group.lower() != "control":
                variant_users.append(users)
        
        # Extracting users in the variant groups after the experiment went live
        variant_df = self.data.filter(
            (pl.col("period")>=experiment_start_date) &  # only dates after the experiment went live
            (pl.col("user_id").is_in(*variant_users)) # Only altering data for users in the variant group(s)
        )

        # Altering the data
        metric_cols = [f"metric_{i}" for i in range(self.n_metrics)]
        variant_dfs = []
        for group, users in experiment_groups.items():
            if group.lower() != "control":
                sub_df = variant_df.filter(pl.col("user_id").is_in(users))
                changes = np.random.normal(1.03, 0.03, size=self.n_metrics)
                for col, change in zip(metric_cols, changes):
                    sub_df = sub_df.with_columns(pl.col(col)*change)
                variant_dfs.append(sub_df)

        # Combining the data back into the original data
        variant_df = pl.concat(variant_dfs)
        control_users_df = self.data.filter((~pl.col("user_id").is_in(*variant_users)) | (pl.col("period")<experiment_start_date))
        df = pl.concat([variant_df, control_users_df]).sort(by=["period", "user_id"])

        # Setting the class variables
        self.data = df
        self.experiment_groups[experiment_name] = experiment_groups

    def add_segment(self, segment_name:str, segment_users:list) -> None:
        """When adding a segment it will be added to the segments variable of the class. This can then be used when plotting and filtering the main data.
        If two segments are called the same it will override.

        Args:
            segment_name (str): The name of the segment.
            segment_users (list): The users who are in the segment, i.e. [1,4,10, 21, etc.]
        """
        self.segments[segment_name] = segment_users

if __name__ == "__main__":
    s = SimulateData(3, 10, 10)
    s.add_segment("Top users", [1,2,5])
    s.add_experiment("Test1", datetime(2024,2,1), experiment_groups={"control": [1,3,5,7,9], "variant": [2,4,6,8,10]})
