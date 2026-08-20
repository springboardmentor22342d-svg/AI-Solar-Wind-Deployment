"""
Global Wind Atlas Client.
Retrieves wind speed and resource quality data.

NOTE: Currently uses coordinate-based simulation until the real
Global Wind Atlas API integration is completed.
"""

import logging
import math

logger = logging.getLogger(__name__)


class GlobalWindAtlasClient:
    """Client for interacting with the Global Wind Atlas API or datasets."""

    def get_wind_speed(self, latitude: float, longitude: float) -> dict:
        """
        Fetches wind speed and wind power density.

        Required Inputs:
            - latitude (float): The geographical latitude in decimal degrees.
            - longitude (float): The geographical longitude in decimal degrees.

        Expected Output Format:
            dict containing:
                - wind_speed_10m (float): Average wind speed at 10m height (m/s)
                - wind_speed_50m (float): Average wind speed at 50m height (m/s)
                - wind_speed_100m (float): Average wind speed at 100m height (m/s)
                - wind_power_density (float): Wind power density (W/m²)

        Possible Failure Conditions:
            - Network connection issues or API timeout
            - Invalid coordinates out of bounds
            - Dataset resolution not available for the given coordinates
        """
        # Coordinate-based simulation: produces deterministic, geographically
        # plausible wind speeds. Coastal and high-latitude regions get higher
        # values; equatorial inland regions get lower values.
        base = 4.0 + abs(latitude) / 20.0 + math.sin(math.radians(longitude)) * 1.5
        wind_10m = round(max(1.5, base * 0.7), 2)
        wind_50m = round(max(2.0, base), 2)
        wind_100m = round(max(2.5, base * 1.2), 2)
        # Wind power density ~ 0.5 * air_density * v^3  (simplified)
        wpd = round(0.5 * 1.225 * (wind_50m ** 3), 2)

        logger.info(
            "GlobalWindAtlas (simulated): lat=%.4f lon=%.4f → ws50m=%.2f m/s",
            latitude, longitude, wind_50m,
        )

        return {
            "wind_speed_10m": wind_10m,
            "wind_speed_50m": wind_50m,
            "wind_speed_100m": wind_100m,
            "wind_power_density": wpd,
        }
