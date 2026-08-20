from app.services.feature_engineering.solar import SolarFeatureExtractor
from app.services.feature_engineering.wind import WindFeatureExtractor
from app.services.feature_engineering.terrain import TerrainFeatureExtractor
from app.services.feature_engineering.infrastructure import InfrastructureFeatureExtractor


class FeatureBuilder:
    def __init__(self):
        self.solar_extractor = SolarFeatureExtractor()
        self.wind_extractor = WindFeatureExtractor()
        self.terrain_extractor = TerrainFeatureExtractor()
        self.infra_extractor = InfrastructureFeatureExtractor()

    def build_features(self, latitude: float, longitude: float) -> dict:
        solar = self.solar_extractor.extract(latitude, longitude)
        wind = self.wind_extractor.extract(latitude, longitude)
        terrain = self.terrain_extractor.extract(latitude, longitude)
        infra = self.infra_extractor.extract(latitude, longitude)

        return {
            "latitude": latitude,
            "longitude": longitude,
            **solar,
            **wind,
            **terrain,
            **infra,
        }
