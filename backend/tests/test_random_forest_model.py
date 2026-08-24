from backend.app.forecasting.time_series_loader import (
    TimeSeriesLoader
)

from backend.app.forecasting.dataset_preparation import (
    DatasetPreparation
)

from backend.app.forecasting.random_forest_model import (
    RandomForestForecastModel
)


def test_random_forest_training():

    loader = TimeSeriesLoader(
        "datasets/nasa_power/solar_power_dataset.csv"
    )

    df = loader.prepare_data()

    dataset = DatasetPreparation(df)

    X, y = dataset.prepare_training_data()

    model = RandomForestForecastModel()

    X_train, X_test, y_train, y_test = model.train(
        X,
        y
    )

    predictions = model.predict(
        X_test
    )

    assert len(predictions) == len(y_test)