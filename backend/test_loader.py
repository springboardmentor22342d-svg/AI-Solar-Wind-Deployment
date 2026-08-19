from app.forecasting.historical_loader import HistoricalDataLoader

loader = HistoricalDataLoader(
    "datasets/nasa_power/solar_history.csv"
)

dataset = loader.get_dataset()

print(dataset.head())

print(dataset.info())