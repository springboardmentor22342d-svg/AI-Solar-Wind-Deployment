from app.data_sources.nasa_power import NasaPowerClient
from app.data_sources.global_solar_atlas import GlobalSolarAtlasClient

class SolarFeatureService:
    def __init__(self, nasa_power_client: NasaPowerClient, solar_atlas_client: GlobalSolarAtlasClient):
        self.nasa_power_client = nasa_power_client
        self.solar_atlas_client = solar_atlas_client

    def get_features(self, latitude: float, longitude: float) -> dict:
        live_data = self.nasa_power_client.fetch(latitude, longitude)
        raster_data = self.solar_atlas_client.fetch(latitude, longitude)

        return {
            "solar_irradiance": live_data.get("solar_irradiance"),
            "solar_irradiance_ghi": raster_data.get("ghi"),
            "solar_irradiance_gti": raster_data.get("gti"),
            "optimum_tilt_angle": raster_data.get("opta"),
        }