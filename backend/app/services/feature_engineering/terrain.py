from app.data_sources.srtm import SRTMClient


class TerrainFeatureEngineering:

    def __init__(self):
        self.srtm_client = SRTMClient()

    def build_features(self, latitude: float, longitude: float):
        return self.srtm_client.get_terrain_data(latitude, longitude)