from backend.app.forecasting.time_series_loader import TimeSeriesLoader
from backend.app.forecasting.dataset_preparation import DatasetPreparation


def test_prepare_training_dataset():

    loader = TimeSeriesLoader(
        "datasets/nasa_power/solar_power_dataset.csv"
    )

    df = loader.prepare_data()

    dataset = DatasetPreparation(df)

    X, y = dataset.prepare_training_data()

    assert len(X) == len(y)

    assert "solar_irradiance" in X.columns
    assert "wind_speed" in X.columns
    assert "temperature" in X.columns
    assert "humidity" in X.columns

    assert len(X.columns) == 8