from app.data_sources.land_use import LandUseClient

class LandUseFeatureService:
    def __init__(self, client: LandUseClient):
        self.client = client

    def get_features(self, latitude: float, longitude: float) -> dict:
        raw = self.client.fetch(latitude, longitude)
        return {
            "forest_pct": raw.get("forest_pct"),
            "net_area_sown_pct": raw.get("net_area_sown_pct"),
            "fallow_land_pct": raw.get("fallow_land_pct"),
            "culturable_wasteland_pct": raw.get("culturable_wasteland_pct"),
        }