"""
Connects the forecasting module with the existing environmental data
pipeline. Combines static site features (from FeatureBuilder) with
historical time-series data (from TimeSeriesDataLoader) into one
unified dataset ready for forecasting models.
"""

import pandas as pd
from app.forecasting.data_loader import TimeSeriesDataLoader
from app.forecasting.feature_extraction import extract_time_features


class ForecastInputPipeline:
    def __init__(self, feature_builder):
        self.feature_builder = feature_builder
        self.data_loader = TimeSeriesDataLoader()

    def prepare_forecast_input(self, latitude: float, longitude: float,
                                start_date: str, end_date: str) -> pd.DataFrame:
        """
        Input: coordinate + historical date range.
        Output: a DataFrame where each row is one historical day,
        enriched with:
            - time-based features (year, month, day, day_of_year, week_number)
            - static site context (elevation, slope, land-use, infrastructure)
              repeated across every row, since these don't vary by date
        """
        # Time-varying data
        historical_df = self.data_loader.load_historical_data(latitude, longitude, start_date, end_date)
        if historical_df.empty:
            return historical_df

        historical_df = extract_time_features(historical_df)

        # Static site context — computed once, since it doesn't change per day
        static_features = self.feature_builder.build(latitude, longitude)
        static_columns_to_include = [
            "elevation", "slope", "forest_pct", "culturable_wasteland_pct",
            "distance_to_road_km", "distance_to_grid_km",
        ]
        for col in static_columns_to_include:
            historical_df[col] = static_features.get(col)

        return historical_df