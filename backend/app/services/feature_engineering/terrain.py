from backend.app.data_sources.srtm import SRTMClient

class TerrainService:

    def __init__(self):
        self.srtm_client = SRTMClient()

    def get_terrain_data(self, latitude: float, longitude: float):
        return self.srtm_client.fetch(latitude, longitude)