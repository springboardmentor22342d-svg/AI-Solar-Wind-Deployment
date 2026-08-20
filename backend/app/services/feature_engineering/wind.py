from app.data_sources.global_wind_atlas import GlobalWindAtlasClient


class WindFeatureExtractor:
    def __init__(self):
        self.client = GlobalWindAtlasClient()

    def extract(self, latitude: float, longitude: float) -> dict:
        data = self.client.get_wind_speed(latitude, longitude) or {}
        return {
            "wind_speed_10m_ms": data.get("wind_speed_10m"),
            "wind_speed_50m_ms": data.get("wind_speed_50m"),
            "wind_speed_100m_ms": data.get("wind_speed_100m"),
            "wind_power_density": data.get("wind_power_density"),
        }
