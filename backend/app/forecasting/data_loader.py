"""
Time-series data loader — fetches historical daily solar/wind data
for a coordinate, preserving chronological order, ready for
forecasting models to consume.
"""

import requests
import pandas as pd


class TimeSeriesDataLoader:
    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

    def load_historical_data(self, latitude: float, longitude: float,
                              start_date: str, end_date: str) -> pd.DataFrame:
        """
        Input:
            latitude, longitude: coordinate
            start_date, end_date: format "YYYYMMDD" (e.g., "20200101")

        Output: a pandas DataFrame with one row per day, sorted
        chronologically (oldest first), containing:
            date, solar_irradiance, wind_speed, temperature
        """
        params = {
            "parameters": "ALLSKY_SFC_SW_DWN,WS50M,T2M",
            "community": "RE",
            "longitude": longitude,
            "latitude": latitude,
            "start": start_date,
            "end": end_date,
            "format": "JSON",
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            return self._parse_response(data)
        except requests.exceptions.RequestException:
            return pd.DataFrame(columns=["date", "solar_irradiance", "wind_speed", "temperature"])

    def _parse_response(self, raw_response: dict) -> pd.DataFrame:
        try:
            params = raw_response["properties"]["parameter"]
            dates = list(params["ALLSKY_SFC_SW_DWN"].keys())

            rows = []
            for date_str in dates:
                rows.append({
                    "date": date_str,
                    "solar_irradiance": params["ALLSKY_SFC_SW_DWN"].get(date_str),
                    "wind_speed": params["WS50M"].get(date_str),
                    "temperature": params["T2M"].get(date_str),
                })

            df = pd.DataFrame(rows)
            df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
            df = df.sort_values("date").reset_index(drop=True)  # preserve chronological order
            return df
        except (KeyError, TypeError):
            return pd.DataFrame(columns=["date", "solar_irradiance", "wind_speed", "temperature"])