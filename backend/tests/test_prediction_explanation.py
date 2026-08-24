


from backend.app.forecasting.time_series_loader import (
    TimeSeriesLoader
)

from backend.app.forecasting.dataset_preparation import (
    DatasetPreparation
)

from backend.app.forecasting.random_forest_model import (
    RandomForestForecastModel
)


def test_prediction_contains_explanation():

    loader = TimeSeriesLoader(
        "datasets/nasa_power/solar_power_dataset.csv"
    )

    df = loader.prepare_data()

    dataset = DatasetPreparation(df)

    X, y = dataset.prepare_training_data()

    model = RandomForestForecastModel()

    model.train(X, y)

    prediction = model.predict(X)

    explanation = model.explain_prediction(
        list(X.columns),
        top_n=3
    )

    # Prediction must exist
    assert prediction is not None
    assert len(prediction) == len(X)

    # Explanation must exist
    assert "top_features" in explanation
    assert "explanation" in explanation

    # Top features must be present
    assert len(explanation["top_features"]) == 3

    # Each feature must contain required fields
    for item in explanation["top_features"]:
        assert "feature" in item
        assert "importance" in item

    # Explanation must be human-readable
    assert isinstance(
        explanation["explanation"],
        str
    )

    assert len(
        explanation["explanation"]
    ) > 0
