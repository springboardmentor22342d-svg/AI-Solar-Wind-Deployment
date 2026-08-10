"""
Solar forecasting — predicts future daily solar irradiance using a
simple, interpretable seasonal-average model as a baseline (matches
the same "start simple" philosophy used for the ML prediction models).
"""

import pandas as pd


class SolarForecastModel:
    def __init__(self):
        self.monthly_averages = None

    def fit(self, historical_df: pd.DataFrame):
        """
        Input: DataFrame with 'month' and 'solar_irradiance' columns
        (output of forecast_input_pipeline.prepare_forecast_input()).
        Learns average solar irradiance per calendar month.
        """
        self.monthly_averages = historical_df.groupby("month")["solar_irradiance"].mean().to_dict()

    def predict(self, month: int) -> float:
        """Returns the forecasted average solar irradiance for a given month (1-12)."""
        if self.monthly_averages is None:
            raise ValueError("Model must be fit() before predicting.")
        return round(self.monthly_averages.get(month, sum(self.monthly_averages.values()) / len(self.monthly_averages)), 4)