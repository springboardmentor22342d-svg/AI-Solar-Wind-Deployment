from app.data_sources.nasa_power import NasaPowerClient
from app.data_sources.global_solar_atlas import GlobalSolarAtlasClient
from app.data_sources.global_wind_atlas import GlobalWindAtlasClient
from app.data_sources.srtm import SrtmClient
from app.data_sources.osm import OsmClient
from app.data_sources.land_use import LandUseClient
from app.data_sources.grid_infrastructure import RoadClient, GridClient

from app.services.feature_engineering.solar import SolarFeatureService
from app.services.feature_engineering.wind import WindFeatureService
from app.services.feature_engineering.terrain import TerrainFeatureService
from app.services.feature_engineering.infrastructure import InfrastructureFeatureService
from app.services.feature_engineering.land_use import LandUseFeatureService
from app.services.feature_engineering.climate import ClimateFeatureService


class FeatureBuilder:
    def __init__(self, solar_service, wind_service, terrain_service, infrastructure_service, land_use_service, climate_service):
        self.solar_service = solar_service
        self.wind_service = wind_service
        self.terrain_service = terrain_service
        self.infrastructure_service = infrastructure_service
        self.land_use_service = land_use_service
        self.climate_service = climate_service

    def build(self, latitude: float, longitude: float) -> dict:
        feature_vector = {"latitude": latitude, "longitude": longitude}
        feature_vector.update(self.solar_service.get_features(latitude, longitude))
        feature_vector.update(self.wind_service.get_features(latitude, longitude))
        feature_vector.update(self.terrain_service.get_features(latitude, longitude))
        feature_vector.update(self.infrastructure_service.get_features(latitude, longitude))
        feature_vector.update(self.land_use_service.get_features(latitude, longitude))
        feature_vector.update(self.climate_service.get_features(latitude, longitude))
        return feature_vector


def create_feature_builder() -> FeatureBuilder:
    nasa_power_client = NasaPowerClient()  # created once, shared by solar + climate services

    return FeatureBuilder(
        solar_service=SolarFeatureService(nasa_power_client, GlobalSolarAtlasClient()),
        wind_service=WindFeatureService(GlobalWindAtlasClient()),
        terrain_service=TerrainFeatureService(SrtmClient()),
        infrastructure_service=InfrastructureFeatureService(OsmClient(), RoadClient(), GridClient()),
        land_use_service=LandUseFeatureService(LandUseClient()),
        climate_service=ClimateFeatureService(nasa_power_client),
    )