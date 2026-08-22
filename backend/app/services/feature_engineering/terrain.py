from app.data_sources.srtm import SrtmClient

class TerrainFeatureService:
    def __init__(self, client: SrtmClient):
        self.client = client

    def get_features(self, latitude: float, longitude: float) -> dict:
        elevation_data = self.client.fetch(latitude, longitude)
        slope_data = self.client.fetch_slope(latitude, longitude)
        return {
            "elevation": elevation_data.get("elevation"),
            "slope": slope_data.get("slope"),
        }