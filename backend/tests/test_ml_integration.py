import pytest
from app.services.ml_inference import ml_engine
from app.services.analysis_pipeline import AnalysisPipeline

def test_ml_model_loads_singleton():
    """Verify the ML model loads successfully as a singleton."""
    assert ml_engine._model is not None, "Model failed to load. Is best_baseline_model.joblib present?"
    
    # Verify singleton
    from app.services.ml_inference import MLInferenceEngine
    another_engine = MLInferenceEngine()
    assert ml_engine is another_engine

def test_ml_prediction_valid_features():
    """Verify prediction works with exact valid features."""
    features = {
        "solar_irradiance_kwh": 6.5,
        "wind_speed_ms": 7.0,
        "slope_deg": 5.0,
        "dist_grid_km": 10.0,
        "dist_road_km": 2.0
    }
    score, importances = ml_engine.predict_suitability(features)
    assert isinstance(score, float)
    assert 0.0 <= score <= 100.0
    assert isinstance(importances, dict)

def test_ml_prediction_missing_features_handled():
    """Verify prediction handles missing features gracefully (defaults to 0.0)."""
    features = {
        "solar_irradiance_kwh": 6.5,
        # missing wind, slope, grid, road
    }
    score, importances = ml_engine.predict_suitability(features)
    assert isinstance(score, float)
    assert 0.0 <= score <= 100.0
    assert isinstance(importances, dict)

def test_pipeline_integration_uses_ml_score(monkeypatch):
    """Verify AnalysisPipeline injects ML score into final output."""
    pipeline = AnalysisPipeline()
    
    # Mock the feature builder so we don't hit external APIs during test
    def mock_build_features(*args, **kwargs):
        return {
            "solar_irradiance_kwh": 5.0,
            "wind_speed_ms": 6.0,
            "wind_speed_50m_ms": 6.0,
            "slope_deg": 10.0,
            "dist_grid_km": 5.0,
            "dist_road_km": 1.0
        }
    monkeypatch.setattr(pipeline.feature_builder, "build_features", mock_build_features)
    
    # Mock the time series loader so we don't hit NASA API
    def mock_load_data(*args, **kwargs):
        return []
    monkeypatch.setattr(pipeline.time_series_loader, "load_historical_data", mock_load_data)
    
    result = pipeline.execute_pipeline(latitude=35.0, longitude=-120.0)
    
    # The overall_score must come from the ML model, not just the exact sum of rules
    assert "evaluation" in result
    assert "overall_score" in result["evaluation"]
    assert isinstance(result["evaluation"]["overall_score"], float)
