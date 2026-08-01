"""
Time-based feature extraction — derives temporal attributes from a
date column, commonly used as inputs for forecasting models to help
capture seasonality and cyclic patterns.
"""

import pandas as pd


def extract_time_features(df: pd.DataFrame, date_column: str = "date") -> pd.DataFrame:
    """
    Input: a DataFrame with a datetime column.
    Output: the same DataFrame with added columns:
        year, month, day, day_of_year, week_number
    """
    df = df.copy()
    df["year"] = df[date_column].dt.year
    df["month"] = df[date_column].dt.month
    df["day"] = df[date_column].dt.day
    df["day_of_year"] = df[date_column].dt.dayofyear
    df["week_number"] = df[date_column].dt.isocalendar().week
    return df