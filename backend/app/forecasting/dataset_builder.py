import pandas as pd


class DatasetBuilder:

    """
    Converts engineered features into
    training features (X) and target (y).
    """

    def __init__(self, dataframe: pd.DataFrame):

        self.dataframe = dataframe.copy()

    def build_dataset(self):

        feature_columns = [

            "month",
            "day",
            "day_of_year",
            "week_of_year",
            "temperature",
            "humidity",
            "wind_speed"

        ]

        target_column = "solar_irradiance"

        X = self.dataframe[feature_columns]

        y = self.dataframe[target_column]

        return X, y