from backend.app.data_sources.osm import OSMClient

class InfrastructureService:

    def __init__(self):
        self.osm_client = OSMClient()

    def get_infrastructure_data(self, min_lat, min_lon, max_lat, max_lon):
        return self.osm_client.fetch(min_lat, min_lon, max_lat, max_lon)