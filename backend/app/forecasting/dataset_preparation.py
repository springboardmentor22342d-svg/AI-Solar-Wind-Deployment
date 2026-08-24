import pandas as pd


class DatasetPreparation:
    """
    Prepare training dataset for forecasting models.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe.copy()

        # Convert date column to datetime
        self.df["date"] = pd.to_datetime(self.df["date"])

        # Extract time-based features
        self.df["year"] = self.df["date"].dt.year
        self.df["month"] = self.df["date"].dt.month
        self.df["day"] = self.df["date"].dt.day
        self.df["day_of_year"] = self.df["date"].dt.dayofyear
        

    def prepare_training_data(self):
        """
        Select input features (X) and target variable (y).
        """

        feature_columns = [
            "temperature",
            "humidity",
            "wind_speed",
            "solar_irradiance",
            "year",
            "month",
            "day",
            "day_of_year"
        ]

        target_column =  [
            "temperature",
            "humidity",
            "wind_speed",
            "solar_irradiance",
            "year",
            "month",
            "day",
            "day_of_year"
        ]

        X = self.df[feature_columns]

        y = self.df[target_column]

        return X, y