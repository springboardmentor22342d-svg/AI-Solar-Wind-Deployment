from backend.app.forecasting.time_series_loader import TimeSeriesLoader


class ForecastingPipeline:
    """
    Connect environmental data to forecasting models.
    """

    def __init__(self, dataset_path: str):
        self.loader = TimeSeriesLoader(dataset_path)

    def prepare_forecasting_input(self):
        """
        Returns processed forecasting features.
        """
        return self.loader.get_features()