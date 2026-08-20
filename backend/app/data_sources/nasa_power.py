import logging
import httpx
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class NasaPowerAPIError(Exception):
    """Exception raised for errors in the NASA POWER API request."""
    pass

class CoordinateValidationError(Exception):
    """Exception raised for invalid coordinates."""
    pass

class NasaPowerClient:
    """Client for interacting with the NASA POWER REST API."""
    
    BASE_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"
    
    def _validate_coordinates(self, latitude: float, longitude: float):
        """Validates that latitude and longitude are within standard geographical bounds."""
        if not (-90.0 <= latitude <= 90.0):
            raise CoordinateValidationError(f"Invalid latitude: {latitude}. Must be between -90 and 90.")
        if not (-180.0 <= longitude <= 180.0):
            raise CoordinateValidationError(f"Invalid longitude: {longitude}. Must be between -180 and 180.")

    def get_solar_irradiance(self, latitude: float, longitude: float) -> Dict[str, Optional[float]]:
        """
        Fetches solar irradiance and related climate factors.
        
        Required Inputs:
            - latitude (float): The geographical latitude in decimal degrees.
            - longitude (float): The geographical longitude in decimal degrees.
            
        Expected Output Format:
            dict containing:
                - solar_irradiance (float): Average annual solar irradiance
                - temperature (float): Average ambient temperature
                - relative_humidity (float): Average relative humidity
                
        Raises:
            CoordinateValidationError: If coordinates are out of bounds.
            NasaPowerAPIError: If the API request fails, times out, or returns invalid data.
        """
        self._validate_coordinates(latitude, longitude)
        
        params = {
            "parameters": "ALLSKY_SFC_SW_DWN,T2M,RH2M",
            "community": "RE",
            "longitude": longitude,
            "latitude": latitude,
            "format": "JSON"
        }
        
        try:
            response = httpx.get(self.BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        except httpx.TimeoutException as e:
            logger.error(f"NASA POWER API request timed out: {e}")
            raise NasaPowerAPIError("NASA POWER API request timed out.") from e
        except httpx.RequestError as e:
            logger.error(f"NASA POWER API request failed: {e}")
            raise NasaPowerAPIError(f"NASA POWER API request failed: {e}") from e
        except ValueError as e:
            logger.error(f"Invalid JSON response from NASA POWER API: {e}")
            raise NasaPowerAPIError("Invalid response format from NASA POWER API.") from e

        try:
            parameters = data.get("properties", {}).get("parameter", {})
            
            # Extract the annual average ("ANN") for each parameter
            solar_irradiance = parameters.get("ALLSKY_SFC_SW_DWN", {}).get("ANN")
            temperature = parameters.get("T2M", {}).get("ANN")
            relative_humidity = parameters.get("RH2M", {}).get("ANN")
            
            # Handle cases where the value might be missing or a missing value flag (e.g., -999.0)
            def clean_value(val):
                return None if val == -999.0 or val is None else float(val)

            return {
                "solar_irradiance": clean_value(solar_irradiance),
                "temperature": clean_value(temperature),
                "relative_humidity": clean_value(relative_humidity)
            }
        except Exception as e:
            logger.error(f"Error parsing NASA POWER API response: {e}")
            raise NasaPowerAPIError("Failed to parse expected data from NASA POWER API response.") from e
