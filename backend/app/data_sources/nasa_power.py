import requests


class NasaPowerClient:

    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

    def get_solar_features(
        self,
        latitude: float,
        longitude: float,
    ):
        """
        Fetch solar-related environmental data
        from the NASA POWER API.
        """

        params = {

            "parameters": "ALLSKY_SFC_SW_DWN,T2M,RH2M",

            "community": "RE",

            "longitude": longitude,

            "latitude": latitude,

            "start": "20250101",

            "end": "20250101",

            "format": "JSON"

        }

        try:

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            parameters = data["properties"]["parameter"]

            return {

                "solar_irradiance": parameters["ALLSKY_SFC_SW_DWN"]["20250101"],

                "temperature": parameters["T2M"]["20250101"],

                "relative_humidity": parameters["RH2M"]["20250101"]

            }

        except requests.exceptions.RequestException as e:

            return {

                "success": False,

                "message": str(e)

            }