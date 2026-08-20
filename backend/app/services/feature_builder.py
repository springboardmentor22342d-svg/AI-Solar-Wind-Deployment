"""
Feature Builder Service.
Coordinates data retrieval from all external data sources.
"""

from app.data_sources.nasa_power import NasaPowerClient
from app.data_sources.global_wind_atlas import GlobalWindAtlasClient
from app.data_sources.srtm import SrtmClient
from app.data_sources.osm import OsmClient


class FeatureBuilder:
    """
    Builds a consolidated feature set for a given location by orchestrating
    calls to external dataset clients.
    """

    def __init__(self):
        self.nasa_client = NasaPowerClient()
        self.gwa_client = GlobalWindAtlasClient()
        self.srtm_client = SrtmClient()
        self.osm_client = OsmClient()

    def build_features(self, latitude: float, longitude: float) -> dict:
        """
        Retrieves and aggregates all location features.
        
        Args:
            latitude (float): Latitude in decimal degrees
            longitude (float): Longitude in decimal degrees
            
        Returns:
            dict: Aggregated features from all datasets
        """
        # Placeholder integration points mapping the service layer to data sources
        solar_data = self.nasa_client.get_solar_irradiance(latitude, longitude)
        wind_data = self.gwa_client.get_wind_speed(latitude, longitude)
        terrain_data = self.srtm_client.get_elevation(latitude, longitude)
        infrastructure_data = self.osm_client.get_infrastructure_proximity(latitude, longitude)

        return {
            "latitude": latitude,
            "longitude": longitude,
            "solar": solar_data,
            "wind": wind_data,
            "terrain": terrain_data,
            "infrastructure": infrastructure_data,
        }

    def get_solar_features(self, latitude: float, longitude: float) -> dict:
        """
        Retrieves only the solar features for a given location.
        
        Args:
            latitude (float): Latitude in decimal degrees
            longitude (float): Longitude in decimal degrees
            
        Returns:
            dict: Extracted solar environmental features
        """
        return self.nasa_client.get_solar_irradiance(latitude, longitude)
