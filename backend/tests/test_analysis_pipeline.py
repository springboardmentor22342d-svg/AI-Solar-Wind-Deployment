import pytest
from unittest.mock import patch, MagicMock
from app.services.analysis_pipeline import AnalysisPipeline

@pytest.fixture
def mock_feature_builder():
    with patch("app.services.analysis_pipeline.FeatureBuilder") as mock:
        yield mock

def test_pipeline_successful_execution(mock_feature_builder):
    # Setup mock data for feature builder
    mock_instance = mock_feature_builder.return_value
    mock_instance.build_features.return_value = {
        "solar_irradiance_kwh": 6.5,
        "temperature_c": 25.0,
        "relative_humidity_pct": 50.0,
        "wind_speed_10m_ms": 6.0,
        "wind_speed_50m_ms": 7.5,
        "wind_speed_100m_ms": 8.0,
        "wind_power_density": 300,
        "elevation_m": 100,
        "slope_deg": 2.0,
        "dist_grid_km": 5.0,
        "dist_road_km": 1.0,
    }

    # Execute pipeline
    pipeline = AnalysisPipeline()
    result = pipeline.execute_pipeline(latitude=20.0, longitude=85.0, site_name="Test Site")

    # Assertions on pipeline calls
    mock_instance.build_features.assert_called_once_with(20.0, 85.0)

    # Assertions on the consolidated result structure
    assert result["site_name"] == "Test Site"
    assert result["latitude"] == 20.0
    assert result["longitude"] == 85.0
    
    # Check features processing
    assert "features" in result
    assert result["features"]["wind_speed_ms"] == 7.5
    assert result["features"]["solar_irradiance_kwh"] == 6.5
    
    # Check evaluation block
    assert "evaluation" in result
    assert "overall_score" in result["evaluation"]
    assert "criteria_evaluation" in result["evaluation"]
    assert result["evaluation"]["criteria_evaluation"]["solar_irradiance"]["status"] == "Pass"
    assert result["evaluation"]["criteria_evaluation"]["wind_speed"]["status"] == "Pass"
    
    # Check deployment block
    assert "deployment" in result
    assert result["deployment"]["recommended_technology"] in ["Solar", "Wind", "Hybrid", "Not Recommended"]
    assert "confidence" in result["deployment"]
    assert "reason" in result["deployment"]

def test_pipeline_missing_features(mock_feature_builder):
    # Setup mock data with missing critical features
    mock_instance = mock_feature_builder.return_value
    mock_instance.build_features.return_value = {}

    pipeline = AnalysisPipeline()
    result = pipeline.execute_pipeline(latitude=10.0, longitude=10.0)

    # Missing features should be defaulted to 0.0 in the pipeline before evaluation
    assert result["features"]["wind_speed_ms"] == 0.0
    assert result["features"]["solar_irradiance_kwh"] == 0.0
    
    # A site with 0 wind and 0 solar should not be recommended
    assert result["deployment"]["recommended_technology"] == "Not Recommended"
    
    # All evaluations should fail
    assert result["evaluation"]["criteria_evaluation"]["solar_irradiance"]["status"] == "Fail"
    assert result["evaluation"]["criteria_evaluation"]["wind_speed"]["status"] == "Fail"
