from app.data_sources.srtm import SrtmClient


class TerrainFeatureExtractor:
    def __init__(self):
        self.client = SrtmClient()

    def extract(self, latitude: float, longitude: float) -> dict:
        data = self.client.get_elevation(latitude, longitude) or {}
        return {
            "elevation_m": data.get("elevation_m"),
            "slope_deg": data.get("slope_deg"),
        }
