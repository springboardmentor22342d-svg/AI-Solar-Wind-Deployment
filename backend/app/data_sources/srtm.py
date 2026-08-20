"""
SRTM (Shuttle Radar Topography Mission) Client.
Retrieves elevation and terrain mapping data.

NOTE: Currently uses coordinate-based simulation until the real
SRTM GeoTIFF data integration is completed.
"""

import logging
import math

logger = logging.getLogger(__name__)


class SrtmClient:
    """Client for retrieving Digital Elevation Model (DEM) data."""

    def get_elevation(self, latitude: float, longitude: float) -> dict:
        """
        Fetches terrain elevation and slope data.

        Required Inputs:
            - latitude (float): The geographical latitude in decimal degrees.
            - longitude (float): The geographical longitude in decimal degrees.

        Expected Output Format:
            dict containing:
                - elevation_m (float): Height above sea level in meters
                - slope_deg (float): Terrain slope in degrees

        Possible Failure Conditions:
            - Local GeoTIFF missing or unreadable
            - Network error if fetching from external service
            - Coordinates fall over ocean or outside mapped area
        """
        # Coordinate-based simulation: higher latitudes and inland areas
        # tend toward higher elevations; slope varies with terrain roughness.
        elevation = abs(latitude) * 8.0 + abs(longitude) * 2.0 + math.sin(latitude * 0.1) * 100
        elevation = round(max(5.0, elevation), 2)

        # Slope: gentle in plains, steeper in mountains
        slope = round(abs(math.sin(math.radians(latitude * 3)) * 8.0 + math.cos(math.radians(longitude * 2)) * 4.0), 2)
        slope = round(max(0.5, min(slope, 25.0)), 2)

        logger.info(
            "SRTM (simulated): lat=%.4f lon=%.4f → elev=%.1fm slope=%.1f°",
            latitude, longitude, elevation, slope,
        )

        return {
            "elevation_m": elevation,
            "slope_deg": slope,
        }
