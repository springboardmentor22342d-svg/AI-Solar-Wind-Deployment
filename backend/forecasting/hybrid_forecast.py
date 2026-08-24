class HybridForecaster:
    def forecast(self,solar_data,wind_data):
        return{
            "technology": "Hybrid",
            "solar_forecast": solar_data,
            "wind_forecast": wind_data
        }