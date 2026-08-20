from app.services.deployment_strategy import build_deployment_recommendation

def test_hybrid_when_both_excellent():
    result = build_deployment_recommendation(6.5, 8.0)
    assert result["deployment"] == "Hybrid"

def test_solar_when_solar_dominant():
    result = build_deployment_recommendation(6.5, 2.0)
    assert result["deployment"] == "Solar"

def test_not_recommended_when_both_poor():
    result = build_deployment_recommendation(2.0, 1.5)
    assert result["deployment"] == "Not Recommended"