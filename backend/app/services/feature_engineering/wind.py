from app.data_sources.global_wind_atlas import GlobalWindAtlasClient

class WindFeatureService:
    def __init__(self, client: GlobalWindAtlasClient):
        self.client = client

    def get_features(self, latitude: float, longitude: float) -> dict:
        raw = self.client.fetch(latitude, longitude)
        return {
            "wind_speed_100m": raw.get("wind_speed_100m"),
            "power_density_100m": raw.get("power_density_100m"),
        }