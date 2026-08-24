import pandas as pd
from pathlib import Path

from backend.app.forecasting.feature_extractor import (
    TimeFeatureExtractor
)

class TimeSeriesLoader:


    def __init__(self, file_path):

        self.file_path = Path(file_path)



    def load_data(self):

        """
        Load historical renewable energy data
        """


        if not self.file_path.exists():

            raise FileNotFoundError(
                "Dataset not found"
            )


        df = pd.read_csv(
            self.file_path
        )


        return df


    def prepare_data(self):

        df = self.load_data()

    # Rename columns if required
        column_mapping = {
        "timestamp": "date",
        "surface_radiation_wm2": "solar_irradiance",
        "air_temperature_c": "temperature",
        "relative_humidity_pct": "humidity"
        }

        df = df.rename(columns=column_mapping)

        df["date"] = pd.to_datetime(df["date"])

        df = df.sort_values("date").reset_index(drop=True)

        df = df.ffill()

    # Extract time-based features
        extractor = TimeFeatureExtractor()
        df = extractor.transform(df)

        return df


    def get_features(self):
    
        df = self.prepare_data()

        features = df[
             [
            "solar_irradiance",
            "temperature",
            "humidity",
            "wind_speed",
            "year",
            "month",
            "day",
            "day_of_year"
            ]
        ]

        return features