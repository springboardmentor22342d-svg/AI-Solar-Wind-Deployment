class WindForecaster:
    def forecast(self,data):
        if "wind_speed" not in data.columns:
            return None
        forecast = data["wind_speed"].mean()
        return{
            "technology":"Wind",
            "forecasted_wind_speed": round(forecast,2)
        }