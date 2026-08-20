import pytest
from app.services.forecasting.feature_extractor import TemporalFeatureExtractor
from app.services.forecasting.solar_forecaster import SolarForecaster
from app.services.forecasting.wind_forecaster import WindForecaster
from app.services.forecasting.hybrid_forecaster import HybridForecaster

def test_temporal_feature_extractor():
    date_str = "20260728"
    features = TemporalFeatureExtractor.extract_features(date_str)
    
    assert features["year"] == 2026
    assert features["month"] == 7
    assert features["day"] == 28
    assert features["day_of_year"] == 209 # approximate depending on leap year

def test_temporal_feature_transformer():
    data = [{"date": "20260728", "solar": 5.0}]
    transformed = TemporalFeatureExtractor.transform_series(data)
    
    assert len(transformed) == 1
    assert "year" in transformed[0]
    assert transformed[0]["year"] == 2026
    assert transformed[0]["solar"] == 5.0

def test_solar_forecaster():
    historical_data = [
        {"date": "20250728", "day_of_year": 209, "solar_irradiance": 6.0},
        {"date": "20250729", "day_of_year": 210, "solar_irradiance": 6.5}
    ]
    forecaster = SolarForecaster()
    predictions = forecaster.forecast(historical_data, days_ahead=2)
    
    assert len(predictions) == 2
    assert "predicted_solar_irradiance" in predictions[0]

def test_wind_forecaster():
    historical_data = [
        {"date": "20250728", "day_of_year": 209, "wind_speed": 4.0},
        {"date": "20250729", "day_of_year": 210, "wind_speed": 4.5}
    ]
    forecaster = WindForecaster()
    predictions = forecaster.forecast(historical_data, days_ahead=2)
    
    assert len(predictions) == 2
    assert "predicted_wind_speed" in predictions[0]

def test_hybrid_forecaster():
    historical_data = [
        {"date": "20250728", "day_of_year": 209, "solar_irradiance": 6.0, "wind_speed": 4.0},
        {"date": "20250729", "day_of_year": 210, "solar_irradiance": 6.5, "wind_speed": 4.5}
    ]
    forecaster = HybridForecaster()
    predictions = forecaster.forecast(historical_data, days_ahead=2)
    
    assert len(predictions) == 2
    assert "predicted_solar_irradiance" in predictions[0]
    assert "predicted_wind_speed" in predictions[0]
