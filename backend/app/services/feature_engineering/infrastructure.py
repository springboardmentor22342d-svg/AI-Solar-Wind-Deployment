from app.data_sources.osm import OsmClient
from app.data_sources.grid_infrastructure import RoadClient, GridClient

class InfrastructureFeatureService:
    def __init__(self, osm_client: OsmClient, road_client: RoadClient, grid_client: GridClient):
        self.osm_client = osm_client
        self.road_client = road_client
        self.grid_client = grid_client

    def get_features(self, latitude: float, longitude: float) -> dict:
        settlement_data = self.osm_client.fetch(latitude, longitude)
        road_data = self.road_client.fetch(latitude, longitude)
        grid_data = self.grid_client.fetch(latitude, longitude)

        return {
            "nearby_settlement_count": settlement_data.get("nearby_settlement_count"),
            "distance_to_nearest_settlement_km": settlement_data.get("distance_to_nearest_settlement_km"),
            "nearest_settlement_name": settlement_data.get("nearest_settlement_name"),
            "distance_to_road_km": road_data.get("distance_to_road_km"),
            "distance_to_grid_km": grid_data.get("distance_to_grid_km"),
        }