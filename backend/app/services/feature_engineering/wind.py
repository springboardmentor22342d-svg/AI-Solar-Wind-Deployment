from app.data_sources.global_wind_atlas import GlobalWindAtlasClient


class WindFeatureEngineering:

    def __init__(self):
        self.wind_client = GlobalWindAtlasClient()

    def build_features(self, latitude: float, longitude: float):
        return self.wind_client.get_wind_data(latitude, longitude)