"""
OpenStreetMap Client.
Retrieves local infrastructure data such as roads and substations.

NOTE: Currently uses coordinate-based simulation until the real
Overpass API / shapefile integration is completed.
"""

import logging
import math

logger = logging.getLogger(__name__)


class OsmClient:
    """Client for querying infrastructure from OpenStreetMap."""

    def get_infrastructure_proximity(self, latitude: float, longitude: float) -> dict:
        """
        Analyzes the distance to nearby infrastructure.

        Required Inputs:
            - latitude (float): The geographical latitude in decimal degrees.
            - longitude (float): The geographical longitude in decimal degrees.

        Expected Output Format:
            dict containing:
                - dist_grid_km (float): Distance to nearest substation/transmission line (km)
                - dist_road_km (float): Distance to nearest road (km)
                - land_cover_class (str): Categorized land cover classification

        Possible Failure Conditions:
            - Overpass API timeout or rate limit
            - Local shapefile missing
            - No infrastructure found within search radius
        """
        # Coordinate-based simulation: more populated/accessible areas
        # (lower latitudes, moderate longitudes) have closer infrastructure.
        dist_grid = round(abs(math.sin(math.radians(latitude * 2))) * 15.0 + abs(math.cos(math.radians(longitude))) * 5.0, 2)
        dist_grid = round(max(0.5, min(dist_grid, 45.0)), 2)

        dist_road = round(abs(math.cos(math.radians(latitude * 3))) * 5.0 + abs(math.sin(math.radians(longitude * 2))) * 3.0, 2)
        dist_road = round(max(0.2, min(dist_road, 20.0)), 2)

        # Simple land cover classification based on coordinates
        lat_mod = int(abs(latitude)) % 10
        if lat_mod < 3:
            land_cover = "cropland"
        elif lat_mod < 6:
            land_cover = "grassland"
        elif lat_mod < 8:
            land_cover = "forest"
        else:
            land_cover = "barren"

        logger.info(
            "OSM (simulated): lat=%.4f lon=%.4f → grid=%.1fkm road=%.1fkm land=%s",
            latitude, longitude, dist_grid, dist_road, land_cover,
        )

        return {
            "dist_grid_km": dist_grid,
            "dist_road_km": dist_road,
            "land_cover_class": land_cover,
        }
