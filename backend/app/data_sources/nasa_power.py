import requests

class NasaPowerClient:
    """
    Live client for the NASA POWER API. Fetches solar irradiance,
    temperature, and relative humidity directly from NASA's servers.
    """

    BASE_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"

    def __init__(self):
        self._cache = {}

    def fetch(self, latitude: float, longitude: float) -> dict:
        key = (round(latitude, 4), round(longitude, 4))
        if key in self._cache:
            return self._cache[key]

        result = self._fetch_from_api(latitude, longitude)
        self._cache[key] = result
        return result

    def _fetch_from_api(self, latitude: float, longitude: float) -> dict:
        params = {
            "parameters": "ALLSKY_SFC_SW_DWN,T2M,RH2M",
            "community": "RE",
            "longitude": longitude,
            "latitude": latitude,
            "format": "JSON",
        }
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return self._extract_parameters(response.json())
        except requests.exceptions.RequestException:
            return self._empty_result()

    def _extract_parameters(self, raw_response: dict) -> dict:
        try:
            params = raw_response["properties"]["parameter"]
            return {
                "solar_irradiance": params["ALLSKY_SFC_SW_DWN"]["ANN"],
                "temperature": params["T2M"]["ANN"],
                "humidity": params["RH2M"]["ANN"],
            }
        except (KeyError, TypeError):
            return self._empty_result()

    def _empty_result(self) -> dict:
        return {"solar_irradiance": None, "temperature": None, "humidity": None}