


from backend.app.feasibility.feasibility import FeasibilityEngine


def test_hard_constraint_violation_rejects_site():

    service = FeasibilityEngine()

    site = {
        "slope": 20,
        "solar_irradiance": 5.5,
        "wind_speed": 6.8,
        "distance_to_grid": 5,
        "distance_to_road": 2,
        "restricted_land": True
    }

    result = service.evaluate(site)

    print("\nHard Constraint Violation:")
    print(result)

    assert result["technically_feasible"] is False
    assert result["hard_constraints"]["feasible"] is False


def test_good_site_is_feasible():

    service = FeasibilityEngine()

    site = {
        "slope": 4,
        "solar_irradiance": 5.5,
        "wind_speed": 6.8,
        "distance_to_grid": 5,
        "distance_to_road": 2,
        "restricted_land": False
    }

    result = service.evaluate(site)

    print("\nGood Site:")
    print(result)

    assert result["technically_feasible"] is True
    assert result["hard_constraints"]["feasible"] is True
    assert result["soft_score"] > 0


def test_poor_accessibility_reduces_score():

    service = FeasibilityEngine()

    good_site = {
        "slope": 4,
        "solar_irradiance": 5.5,
        "wind_speed": 6.8,
        "distance_to_grid": 5,
        "distance_to_road": 2,
        "restricted_land": False
    }

    poor_access_site = {
        "slope": 4,
        "solar_irradiance": 5.5,
        "wind_speed": 6.8,
        "distance_to_grid": 18,
        "distance_to_road": 9,
        "restricted_land": False
    }

    good_result = service.evaluate(good_site)
    poor_result = service.evaluate(poor_access_site)

    print("\nGood Site Score:", good_result["soft_score"])
    print("Poor Accessibility Score:", poor_result["soft_score"])

    assert good_result["technically_feasible"] is True
    assert poor_result["technically_feasible"] is True

    assert poor_result["soft_score"] < good_result["soft_score"]
