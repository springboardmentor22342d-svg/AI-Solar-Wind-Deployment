import pandas as pd


class TimeSeriesLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        """
        Load historical renewable energy data.
        """

        df = pd.read_csv(self.file_path)

        # Convert date column to datetime
        df["date"] = pd.to_datetime(df["date"])

        # Preserve chronological order
        df = df.sort_values("date")

        # Reset index
        df = df.reset_index(drop=True)

        return df