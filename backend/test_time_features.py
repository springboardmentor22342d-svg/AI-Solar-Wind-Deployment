from app.forecasting.historical_loader import HistoricalDataLoader
from app.forecasting.time_feature_extractor import TimeFeatureExtractor


loader = HistoricalDataLoader(
    "datasets/nasa_power/solar_history.csv"
)

dataset = loader.get_dataset()

extractor = TimeFeatureExtractor()

features = extractor.transform(dataset)

print(features.head())

print(features.columns)