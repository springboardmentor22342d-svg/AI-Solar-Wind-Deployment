"""
Hybrid forecasting — combines solar and wind seasonal forecasts into
a single monthly outlook, for site-level planning.
"""

from app.forecasting.solar_forecast import SolarForecastModel
from app.forecasting.wind_forecast import WindForecastModel


class HybridForecastModel:
    def __init__(self):
        self.solar_model = SolarForecastModel()
        self.wind_model = WindForecastModel()

    def fit(self, historical_df):
        self.solar_model.fit(historical_df)
        self.wind_model.fit(historical_df)

    def predict(self, month: int) -> dict:
        return {
            "month": month,
            "forecasted_solar_irradiance": self.solar_model.predict(month),
            "forecasted_wind_speed": self.wind_model.predict(month),
        }