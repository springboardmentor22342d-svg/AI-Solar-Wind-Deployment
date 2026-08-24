from backend.app.forecasting.forecasting_pipeline import (
    ForecastingPipeline
)


def test_forecasting_pipeline():

    pipeline = ForecastingPipeline(
         "datasets/nasa_power/solar_power_dataset.csv"
    )

    features = pipeline.prepare_forecasting_input()

    assert len(features) > 0

    assert "solar_irradiance" in features.columns
    assert "wind_speed" in features.columns
    assert "year" in features.columns
    assert "month" in features.columns