import pandas as pd


class TimeFeatureExtractor:

    def transform(self, dataframe: pd.DataFrame):

        df = dataframe.copy()

        # Date is already parsed by HistoricalDataLoader

        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["day"] = df["date"].dt.day
        df["day_of_week"] = df["date"].dt.dayofweek
        df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
        df["day_of_year"] = df["date"].dt.dayofyear
        df["quarter"] = df["date"].dt.quarter
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

        return df