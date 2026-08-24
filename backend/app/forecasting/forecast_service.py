from .solar_forecast import forecast_solar_energy
from .wind_forecast import forecast_wind_energy
from .hybrid_forecast import forecast_hybrid_energy



class ForecastService:


    def generate_forecast(
            self,
            deployment_type,
            capacity_kw,
            solar,
            wind
    ):


        if deployment_type == "Solar":

            return forecast_solar_energy(
                capacity_kw,
                solar
            )


        elif deployment_type == "Wind":

            return forecast_wind_energy(
                capacity_kw,
                wind
            )


        elif deployment_type == "Hybrid":

            return forecast_hybrid_energy(
                capacity_kw,
                solar,
                wind
            )


        else:

            raise ValueError(
                "Invalid deployment type"
            )