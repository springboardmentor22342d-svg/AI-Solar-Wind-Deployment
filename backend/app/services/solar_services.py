from app.data_sources.nasa_power import NASAPowerClient
class SolarFeatureService:
    def __init__(self):
        self.client = NASAPowerClient()
    def get_features(self,latitude: float, longitude: float):
        data = self.client.get_solar_data(latitude,longitude)
        return self.client.extract_features(data)