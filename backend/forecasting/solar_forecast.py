class SolarForecaster:
    def forecast(self,data):
        if "solar_irradiance" not in data.columns:
            return None
        forecast = data["solar_irradiance"].mean()
        return{
            "technology": "Solar",
            "forecasted_irradiance": round(forecast,2)
        }