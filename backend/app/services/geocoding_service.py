import requests


class GeocodingService:

    def get_coordinates(
        self,
        village: str,
        district: str,
        state: str,
        country: str
    ):

        address = f"{village}, {district}, {state}, {country}"

        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": address,
            "format": "json",
            "limit": 1
        }

        headers = {
            "User-Agent": "SolarWindDeploymentPlatform/1.0"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if not data:
            raise ValueError(
                "Location could not be found"
            )

        return {
            "latitude": float(data[0]["lat"]),
            "longitude": float(data[0]["lon"]),
            "display_name": data[0]["display_name"]
        }