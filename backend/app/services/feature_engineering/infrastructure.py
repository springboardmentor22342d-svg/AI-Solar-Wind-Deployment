from app.data_sources.osm import OSMClient


class InfrastructureFeatureEngineering:

    def __init__(self):
        self.osm_client = OSMClient()

    def build_features(self, latitude: float, longitude: float):
        return self.osm_client.get_infrastructure_data(latitude, longitude)