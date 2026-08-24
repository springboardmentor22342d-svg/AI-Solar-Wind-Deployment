from backend.app.data_sources.nasa_power import NasaPowerClient


class SolarService:

    def __init__(self):
        self.client = NasaPowerClient()

    def get_solar_data(self, latitude: float, longitude: float):
        return self.client.fetch(latitude, longitude)
    


    