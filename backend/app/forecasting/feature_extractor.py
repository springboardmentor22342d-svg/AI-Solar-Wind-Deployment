import pandas as pd


class TimeFeatureExtractor:
    """
    Extract time-based features from a datetime column.
    """

    def __init__(self, date_column: str = "date"):
        self.date_column = date_column

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Generate time-based forecasting features.
        """

        if self.date_column not in df.columns:
            raise ValueError(
                f"'{self.date_column}' column not found."
            )

        df = df.copy()

        # Ensure datetime format
        df[self.date_column] = pd.to_datetime(df[self.date_column])

        # Time-based features
        df["year"] = df[self.date_column].dt.year
        df["month"] = df[self.date_column].dt.month
        df["day"] = df[self.date_column].dt.day
        df["day_of_year"] = df[self.date_column].dt.dayofyear

        # Optional week number
        df["week"] = (
            df[self.date_column]
            .dt.isocalendar()
            .week
            .astype(int)
        )

        return df