from backend.app.feasibility.feasibility import FeasibilityEngine


def test_feasible_site():

    features = {
        "solar_irradiance": 5.5,
        "wind_speed": 6.8,
        "slope": 4,
        "distance_to_grid": 6,
        "distance_to_road": 2
    }

    engine = FeasibilityEngine()

    result = engine.evaluate(features)

    assert "technically_feasible" in result
    assert "hard_constraints" in result
    assert "soft_score" in result
    assert "decision" in result

    assert result["technically_feasible"] is True
    assert result["soft_score"] >= 0
    assert result["soft_score"] <= 100


def test_infeasible_site():

    features = {
        "solar_irradiance": 2.0,
        "wind_speed": 2.0,
        "slope": 25,
        "distance_to_grid": 50,
        "distance_to_road": 20
    }

    engine = FeasibilityEngine()

    result = engine.evaluate(features)

    assert result["technically_feasible"] is False
    assert len(
        result["hard_constraints"]["failed_constraints"]
    ) > 0