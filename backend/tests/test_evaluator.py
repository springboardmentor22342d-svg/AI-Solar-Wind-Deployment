from backend.app.evaluation.evaluator import (
    EvaluationService
)


def test_evaluation_service_returns_structured_result():

    service = EvaluationService()

    features = {
        "solar_irradiance": 5.8,
        "wind_speed": 6.2,
        "slope": 2.1,
        "distance_to_grid": 4.0,
        "distance_to_road": 2.0,
    }

    result = service.evaluate(features)

    assert "constraints_satisfied" in result
    assert "overall_score" in result
    assert "recommendation" in result
    assert "failed_constraints" in result


def test_valid_features_have_no_failed_constraints():

    service = EvaluationService()

    features = {
        "solar_irradiance": 5.8,
        "wind_speed": 6.2,
        "slope": 2.1,
        "distance_to_grid": 4.0,
        "distance_to_road": 2.0,
    }

    result = service.evaluate(features)

    assert result["constraints_satisfied"] is True
    assert result["failed_constraints"] == []


def test_invalid_features_explain_failed_constraints():

    service = EvaluationService()

    features = {
        "solar_irradiance": 3.0,
        "wind_speed": 2.0,
        "slope": 20.0,
        "distance_to_grid": 15.0,
        "distance_to_road": 8.0,
    }

    result = service.evaluate(features)

    assert result["constraints_satisfied"] is False

    assert len(
        result["failed_constraints"]
    ) == 5