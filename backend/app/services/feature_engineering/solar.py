from app.data_sources.nasa_power import NasaPowerClient


class SolarFeatureEngineering:

    def __init__(self):
        self.nasa_client = NasaPowerClient()

    def build_features(
        self,
        latitude: float,
        longitude: float,
    ):

        return self.nasa_client.get_solar_features(
            latitude,
            longitude,
        )