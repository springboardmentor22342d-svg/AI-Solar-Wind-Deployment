from forecasting.data_loader import TimeSeriesLoader
from forecasting.feature_extractor import TimeFeatureExtractor
from forecasting.solar_forecast import SolarForecaster
from forecasting.wind_forecast import WindForecaster
from forecasting.hybrid_forecast import HybridForecaster

class ForecastingPipeline:

    def __init__(self):
        self.loader = TimeSeriesLoader("data/historical_data.csv")
        self.extractor = TimeFeatureExtractor()
        self.solar = SolarForecaster()
        self.wind = WindForecaster()
        self.hybrid = HybridForecaster()

    def prepare_data(self, file_path):

        self.loader.file_path = file_path

        data = self.loader.load_data()

        data = self.extractor.extract_feature(data)

        solar_result = self.solar.forecast(data)
        wind_result = self.wind.forecast(data)
        hybrid_result = self.hybrid.forecast(solar_result, wind_result)

        return {
            "solar": solar_result,
            "wind": wind_result,
            "hybrid": hybrid_result
        }