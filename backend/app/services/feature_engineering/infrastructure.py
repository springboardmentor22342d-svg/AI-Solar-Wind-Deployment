from app.data_sources.osm import OsmClient


class InfrastructureFeatureExtractor:
    def __init__(self):
        self.client = OsmClient()

    def extract(self, latitude: float, longitude: float) -> dict:
        data = self.client.get_infrastructure_proximity(latitude, longitude) or {}
        return {
            "dist_grid_km": data.get("dist_grid_km"),
            "dist_road_km": data.get("dist_road_km"),
        }
