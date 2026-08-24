from backend.app.feasibility.hard_constraints import (
    HardConstraintValidator
)


def test_valid_site_passes_hard_constraints():

    features = {
        "solar_irradiance": 5.5,
        "wind_speed": 6.8,
        "slope": 4,
        "distance_to_grid": 6,
        "distance_to_road": 2
    }

    validator = HardConstraintValidator()

    result = validator.validate(features)

    print(result)

    assert result["feasible"] is True
    assert result["failed_constraints"] == []


def test_excessive_slope_fails():

    features = {
        "solar_irradiance": 5.5,
        "wind_speed": 6.8,
        "slope": 25,
        "distance_to_grid": 6,
        "distance_to_road": 2
    }

    validator = HardConstraintValidator()

    result = validator.validate(features)

    print(result)

    assert result["feasible"] is False
    assert "Unacceptable terrain slope" in result["failed_constraints"]


def test_low_solar_fails():

    features = {
        "solar_irradiance": 2.5,
        "wind_speed": 6.8,
        "slope": 4,
        "distance_to_grid": 6,
        "distance_to_road": 2
    }

    validator = HardConstraintValidator()

    result = validator.validate(features)

    print(result)

    assert result["feasible"] is False
    assert "Insufficient solar irradiance" in result["failed_constraints"]
    