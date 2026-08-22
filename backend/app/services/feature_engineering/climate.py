from app.data_sources.nasa_power import NasaPowerClient

class ClimateFeatureService:
    def __init__(self, client: NasaPowerClient):
        self.client = client

    def get_features(self, latitude: float, longitude: float) -> dict:
        raw = self.client.fetch(latitude, longitude)
        return {
            "temperature": raw.get("temperature"),
            "humidity": raw.get("humidity"),
        }