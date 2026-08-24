
import requests


class NasaPowerClient:

    BASE_URL = "https://power.larc.nasa.gov/api/temporal/climatology/point"

    def fetch(self, latitude: float, longitude: float):

        params = {
            "parameters": "ALLSKY_SFC_SW_DWN,T2M,RH2M",
            "community": "RE",
            "longitude": longitude,
            "latitude": latitude,
            "format": "JSON"
        }

  

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            # Extract the required parameters
            parameters = data["properties"]["parameter"]

            return {
                "solar_irradiance": parameters["ALLSKY_SFC_SW_DWN"]["ANN"],
                "temperature": parameters["T2M"]["ANN"],
                "humidity": parameters["RH2M"]["ANN"]
            }

        except requests.exceptions.Timeout:
            print("NASA POWER API request timed out.")
            return None

        except requests.exceptions.ConnectionError:
            print("Could not connect to NASA POWER API.")
            return None

        except requests.exceptions.RequestException as error:
            print(f"NASA POWER API request failed: {error}")
            return None

        except (ValueError, KeyError) as error:
            print(f"NASA POWER response data is invalid: {error}")
            return None
    