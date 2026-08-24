from backend.app.forecasting.time_series_loader import (
    TimeSeriesLoader
)


DATASET_PATH = "datasets/nasa_power/solar_power_dataset.csv"



def test_load_timeseries():

    loader = TimeSeriesLoader(
        DATASET_PATH
    )

    data = loader.load_data()

    assert len(data) > 0



def test_chronological_order():

    loader = TimeSeriesLoader(
        DATASET_PATH
    )

    data = loader.prepare_data()

    assert (
        data["date"].is_monotonic_increasing
    )



def test_forecasting_features():

    loader = TimeSeriesLoader(
        DATASET_PATH
    )

    features = loader.get_features()

    assert (
        "solar_irradiance"
        in features.columns
    )

    assert (
        "wind_speed"
        in features.columns
    )