from app.evaluation.evaluator import evaluate_site

def test_good_site_passes():
    features = {"solar_irradiance": 5.2, "wind_speed": 4.9, "slope": 3.5,
                "distance_to_grid_km": 2.0, "distance_to_road_km": 1.5,
                "forest_pct": 20.0, "culturable_wasteland_pct": 15.0}
    result = evaluate_site(features)
    assert result["hard_constraints_passed"] is True
    assert result["suitability_score"] > 0

def test_bad_site_fails():
    features = {"solar_irradiance": 3.2, "wind_speed": 2.0, "slope": 25.0,
                "distance_to_grid_km": 80.0, "distance_to_road_km": 1.5,
                "forest_pct": 20.0, "culturable_wasteland_pct": 15.0}
    result = evaluate_site(features)
    assert result["hard_constraints_passed"] is False
    assert result["suitability_score"] == 0