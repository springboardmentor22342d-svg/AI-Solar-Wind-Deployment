"""
Wind forecasting — predicts future daily wind speed using a simple
seasonal-average baseline, mirroring solar_forecast.py's approach.
"""

import pandas as pd


class WindForecastModel:
    def __init__(self):
        self.monthly_averages = None

    def fit(self, historical_df: pd.DataFrame):
        """
        Input: DataFrame with 'month' and 'wind_speed' columns.
        """
        self.monthly_averages = historical_df.groupby("month")["wind_speed"].mean().to_dict()

    def predict(self, month: int) -> float:
        if self.monthly_averages is None:
            raise ValueError("Model must be fit() before predicting.")
        return round(self.monthly_averages.get(month, sum(self.monthly_averages.values()) / len(self.monthly_averages)), 4)