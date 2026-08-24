from backend.app.services.feature_engineering.solar import SolarService
from backend.app.services.feature_engineering.wind import WindService
from backend.app.services.feature_engineering.terrain import TerrainService
from backend.app.services.feature_engineering.infrastructure import InfrastructureService


class FeatureBuilder:

    def __init__(self):
        self.solar_service = SolarService()
        self.wind_service = WindService()
        self.terrain_service = TerrainService()
        self.infrastructure_service = InfrastructureService()

    def build_features(self, latitude: float, longitude: float):

        # Placeholder calls
        solar_data = self.solar_service.get_solar_data(latitude, longitude)

        wind_data = self.wind_service.get_wind_data(latitude, longitude)

        terrain_data = self.terrain_service.get_terrain_data(latitude, longitude)

        infrastructure_data = self.infrastructure_service.get_infrastructure_data(
            latitude,
            longitude,
            latitude,
            longitude
        )

        # Feature engineering logic will be implemented later
        return {
            "solar": solar_data,
            "wind": wind_data,
            "terrain": terrain_data,
            "infrastructure": infrastructure_data
        }