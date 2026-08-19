from app.services.feature_engineering.solar import SolarFeatureEngineering
from app.services.feature_engineering.wind import WindFeatureEngineering
from app.services.feature_engineering.terrain import TerrainFeatureEngineering
from app.services.feature_engineering.infrastructure import InfrastructureFeatureEngineering


class FeatureBuilder:

    def __init__(self):

        self.solar = SolarFeatureEngineering()

        self.wind = WindFeatureEngineering()

        self.terrain = TerrainFeatureEngineering()

        self.infrastructure = InfrastructureFeatureEngineering()

    def build(self, latitude: float, longitude: float):

        solar_features = self.solar.build_features(latitude, longitude)

        wind_features = self.wind.build_features(latitude, longitude)

        terrain_features = self.terrain.build_features(latitude, longitude)

        infrastructure_features = self.infrastructure.build_features(
            latitude,
            longitude
        )

        return {
            "solar": solar_features,
            "wind": wind_features,
            "terrain": terrain_features,
            "infrastructure": infrastructure_features
        }