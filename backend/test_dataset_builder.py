from app.forecasting.historical_loader import HistoricalDataLoader
from app.forecasting.time_feature_extractor import TimeFeatureExtractor
from app.forecasting.dataset_builder import DatasetBuilder

loader = HistoricalDataLoader(
    "datasets/nasa_power/solar_history.csv"
)

dataset = loader.get_dataset()

extractor = TimeFeatureExtractor()

dataset = extractor.transform(dataset)

builder = DatasetBuilder(dataset)

X, y = builder.build_dataset()

print(X.head())

print()

print(y.head())

print()

print(X.shape)

print(y.shape)