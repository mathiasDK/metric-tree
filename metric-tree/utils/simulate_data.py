import numpy as np
import polars as pl
from datetime import datetime, timedelta

np.random.seed(42) # Ensuring similar datasets

class SimulateData:
    def __init__(self, n_metrics:int, n_periods:int, n_users:int) -> None:
        self.n_metrics = n_metrics
        self.n_periods = n_periods
        self.n_users = n_users
        self.experiment_groups = {}
        self._create_dataset()

    def _create_dataset(self):

        # Creating the base data with some covariance
        metric_means = np.random.uniform(10, 100, size=self.n_metrics)
        metric_cov_base = np.random.rand(self.n_metrics, self.n_metrics)
        metric_cov = np.dot(metric_cov_base, metric_cov_base.transpose())
        data = np.random.multivariate_normal(metric_means, metric_cov, (self.n_users, self.n_periods)) # shape(n_users, n_periods, n_metrics)

        # List of user ids and periods
        user_ids = np.linspace(1, self.n_users, self.n_users)
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

    def add_experiment(self, experiment_name:str, experiment_start_date:str, experiment_size:int):
        pass