import os
import requests
import pandas as pd


class NASAHistoricalService:

    BASE_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

    def fetch_historical_data(
        self,
        latitude: float,
        longitude: float,
        start_date: str,
        end_date: str,
    ):

        parameters = [
            "ALLSKY_SFC_SW_DWN",
            "WS2M",
            "T2M",
            "RH2M"
        ]

        params = {
            "parameters": ",".join(parameters),
            "community": "RE",
            "latitude": latitude,
            "longitude": longitude,
            "start": start_date,
            "end": end_date,
            "format": "JSON"
        }

        response = requests.get(
            self.BASE_URL,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        return response.json()
    def json_to_dataframe(self, data):

        parameter_data = data["properties"]["parameter"]

        dates = list(parameter_data["ALLSKY_SFC_SW_DWN"].keys())

        rows = []

        for date in dates:

            rows.append({

                "date": date,

                "solar_irradiance":
                    parameter_data["ALLSKY_SFC_SW_DWN"][date],

                "wind_speed":
                    parameter_data["WS2M"][date],

                "temperature":
                    parameter_data["T2M"][date],

                "humidity":
                    parameter_data["RH2M"][date]

            })

        return pd.DataFrame(rows)
    def save_dataset(
        self,
        dataframe,
        filename,
    ):

        os.makedirs(
            "datasets/nasa_power",
            exist_ok=True
        )

        path = f"datasets/nasa_power/{filename}"

        dataframe.to_csv(
            path,
            index=False
        )

        return path
    def create_dataset(

        self,

        latitude,

        longitude,

        start_date,

        end_date,

        filename,

    ):

        data = self.fetch_historical_data(

            latitude,

            longitude,

            start_date,

            end_date,

        )

        dataframe = self.json_to_dataframe(data)

        return self.save_dataset(

            dataframe,

            filename,

        )