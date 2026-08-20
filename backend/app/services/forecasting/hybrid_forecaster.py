import logging
from typing import List, Dict, Any
from app.services.forecasting.solar_forecaster import SolarForecaster
from app.services.forecasting.wind_forecaster import WindForecaster

logger = logging.getLogger(__name__)

class HybridForecaster:
    """
    Predicts future solar and wind potential based on historical data.
    Combines outputs from both Solar and Wind forecasters.
    """
    def __init__(self):
        self.solar_forecaster = SolarForecaster()
        self.wind_forecaster = WindForecaster()

    def forecast(self, historical_data: List[Dict[str, Any]], days_ahead: int = 30) -> List[Dict[str, Any]]:
        solar_predictions = self.solar_forecaster.forecast(historical_data, days_ahead)
        wind_predictions = self.wind_forecaster.forecast(historical_data, days_ahead)

        hybrid_predictions = []
        for s_pred, w_pred in zip(solar_predictions, wind_predictions):
            if s_pred["date"] == w_pred["date"]:
                hybrid_predictions.append({
                    "date": s_pred["date"],
                    "predicted_solar_irradiance": s_pred["predicted_solar_irradiance"],
                    "predicted_wind_speed": w_pred["predicted_wind_speed"],
                })

        return hybrid_predictions
