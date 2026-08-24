import requests


class NASAPowerClient:

    BASE_URL = (
        "https://power.larc.nasa.gov/api/temporal/daily/point"
    )

    # =========================================================
    # GET NASA POWER DATA
    # =========================================================

    def get_solar_data(
        self,
        latitude: float,
        longitude: float
    ):

        params = {
            # Solar + Temperature + Humidity + Wind Speed
            "parameters": (
                "ALLSKY_SFC_SW_DWN,"
                "T2M,"
                "RH2M,"
                "WS10M"
            ),

            "community": "RE",

            "longitude": longitude,

            "latitude": latitude,

            # Historical data range
            "start": "20240101",

            "end": "20240131",

            "format": "JSON"
        }

        try:

            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=15
            )

            response.raise_for_status()

            return response.json()

        except requests.exceptions.RequestException as e:

            raise Exception(
                f"NASA POWER API ERROR: {e}"
            )


    # =========================================================
    # EXTRACT FEATURES
    # =========================================================

    def extract_features(self, data):

        try:

            parameters = (
                data["properties"]["parameter"]
            )

            return {

                # Solar irradiance
                "solar_irradiance":
                    parameters.get(
                        "ALLSKY_SFC_SW_DWN",
                        {}
                    ),

                # Temperature
                "temperature":
                    parameters.get(
                        "T2M",
                        {}
                    ),

                # Relative humidity
                "relative_humidity":
                    parameters.get(
                        "RH2M",
                        {}
                    ),

                # Wind speed at 10 meters
                "wind_speed":
                    parameters.get(
                        "WS10M",
                        {}
                    ),
            }

        except KeyError as e:

            raise Exception(
                f"NASA POWER response is missing "
                f"expected data: {e}"
            )