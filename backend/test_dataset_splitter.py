from app.forecasting.historical_loader import HistoricalDataLoader
from app.forecasting.time_feature_extractor import TimeFeatureExtractor
from app.forecasting.dataset_builder import DatasetBuilder
from app.forecasting.dataset_splitter import DatasetSplitter

loader = HistoricalDataLoader(
    "datasets/nasa_power/solar_history.csv"
)

dataset = loader.get_dataset()

extractor = TimeFeatureExtractor()

dataset = extractor.transform(dataset)

builder = DatasetBuilder(dataset)

X, y = builder.build_dataset()

splitter = DatasetSplitter()

result = splitter.split(X, y)

print("Training")

print(result["X_train"].shape)

print()

print("Validation")

print(result["X_validation"].shape)

print()

print("Testing")

print(result["X_test"].shape)