

from backend.app.forecasting.time_series_loader import (
    TimeSeriesLoader
)

from backend.app.forecasting.dataset_preparation import (
    DatasetPreparation
)

from backend.app.forecasting.random_forest_model import (
    RandomForestForecastModel
)


def test_feature_importance():

    loader = TimeSeriesLoader(
        "datasets/nasa_power/solar_power_dataset.csv"
    )

    df = loader.prepare_data()

    dataset = DatasetPreparation(df)

    X, y = dataset.prepare_training_data()

    model = RandomForestForecastModel()

    model.train(
        X,
        y
    )

    feature_names = list(X.columns)

    importance = model.get_feature_importance(
        feature_names
    )

    # Check that all features are present
    assert len(importance) == len(feature_names)

    # Check feature names
    returned_features = [
        item["feature"]
        for item in importance
    ]

    assert set(returned_features) == set(
        feature_names
    )

    # Check importance values
    for item in importance:
        assert 0 <= item["importance"] <= 1

    # Check descending order
    scores = [
        item["importance"]
        for item in importance
    ]

    assert scores == sorted(
        scores,
        reverse=True
    )


    def test_feature_importance_is_reasonable():

     loader = TimeSeriesLoader(
        "datasets/nasa_power/solar_power_dataset.csv"
    )

    df = loader.prepare_data()

    dataset = DatasetPreparation(df)

    X, y = dataset.prepare_training_data()

    model = RandomForestForecastModel()

    model.train(X, y)

    importance = model.get_feature_importance(
        list(X.columns)
    )

    print("\nFeature Importance Ranking:")

    for item in importance:
        print(
        f"{item['feature']}: "
        f"{item['importance']:.4f}"
    )

    importance_dict = {
        item["feature"]: item["importance"]
        for item in importance
    }

    # Important renewable-energy features
    assert "solar_irradiance" in importance_dict
    assert "wind_speed" in importance_dict

    # All importance values must be valid
    assert all(
        0 <= value <= 1
        for value in importance_dict.values()
    )

    # Importance should sum approximately to 1
    assert abs(
        sum(importance_dict.values()) - 1.0
    ) < 0.001
