import pandas as pd


class HistoricalDataLoader:

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):

        df = pd.read_csv(self.file_path)

        return df

    def clean(self, df):

        df = df.drop_duplicates()

        df = df.dropna()

        return df

    def sort(self, df):

        df["date"] = pd.to_datetime(
            df["date"].astype(str),
            format="%Y%m%d"
        )

        df = df.sort_values("date")

        df.reset_index(drop=True, inplace=True)

        return df

    def get_dataset(self):

        df = self.load()

        df = self.clean(df)

        df = self.sort(df)

        return df