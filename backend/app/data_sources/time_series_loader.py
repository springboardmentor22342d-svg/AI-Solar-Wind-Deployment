import logging
import httpx
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class TimeSeriesDataLoaderError(Exception):
    pass

class TimeSeriesDataLoader:
    """
    Loads historical renewable energy data (NASA POWER daily point API) and
    prepares it for forecasting. Preserves chronological ordering.
    """
    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

    def load_historical_data(
        self, latitude: float, longitude: float, days_back: int = 365
    ) -> List[Dict[str, Any]]:
        """
        Fetches daily time-series data for the specified coordinates.
        Returns a chronologically ordered list of dictionaries.
        """
        end_date = datetime.now(timezone.utc)
        start_date = end_date - timedelta(days=days_back)

        start_str = start_date.strftime("%Y%m%d")
        end_str = end_date.strftime("%Y%m%d")

        params = {
            "parameters": "ALLSKY_SFC_SW_DWN,WS50M,T2M",
            "community": "RE",
            "longitude": longitude,
            "latitude": latitude,
            "start": start_str,
            "end": end_str,
            "format": "JSON"
        }

        try:
            response = httpx.get(self.BASE_URL, params=params, timeout=15.0)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logger.warning(f"Failed to fetch time series from NASA POWER: {e}. Returning mock time series.")
            return self._generate_mock_time_series(start_date, days_back)

        try:
            properties = data.get("properties", {}).get("parameter", {})
            solar_dict = properties.get("ALLSKY_SFC_SW_DWN", {})
            wind_dict = properties.get("WS50M", {})
            temp_dict = properties.get("T2M", {})

            # Dates are keys like "YYYYMMDD"
            dates = sorted(list(solar_dict.keys()))

            time_series = []
            for date_str in dates:
                # Handle NASA POWER missing data flags
                def clean_value(val):
                    return None if val == -999.0 or val is None else float(val)

                time_series.append({
                    "date": date_str,
                    "solar_irradiance": clean_value(solar_dict.get(date_str)),
                    "wind_speed": clean_value(wind_dict.get(date_str)),
                    "temperature": clean_value(temp_dict.get(date_str)),
                })
            return time_series
        except Exception as e:
            logger.error(f"Error parsing time series data: {e}")
            raise TimeSeriesDataLoaderError("Failed to parse time series data.") from e

    def _generate_mock_time_series(self, start_date: datetime, days: int) -> List[Dict[str, Any]]:
        """Fallback mock data generator if API fails."""
        time_series = []
        for i in range(days):
            current = start_date + timedelta(days=i)
            date_str = current.strftime("%Y%m%d")
            time_series.append({
                "date": date_str,
                "solar_irradiance": 5.0 + (i % 10) / 10.0,
                "wind_speed": 6.0 + (i % 5) / 5.0,
                "temperature": 20.0 + (i % 15) / 5.0,
            })
        return time_series
