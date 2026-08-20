from app.data_sources.nasa_power import NasaPowerClient


class SolarFeatureExtractor:
    def __init__(self):
        self.client = NasaPowerClient()

    def extract(self, latitude: float, longitude: float) -> dict:
        data = self.client.get_solar_irradiance(latitude, longitude)
        return {
            "solar_irradiance_kwh": data.get("solar_irradiance"),
            "temperature_c": data.get("temperature"),
            "relative_humidity_pct": data.get("relative_humidity"),
        }
