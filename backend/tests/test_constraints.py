from backend.app.evaluation.constraints import (
    is_slope_acceptable,
    has_sufficient_solar_irradiance,
    has_sufficient_wind_speed,
    is_within_grid_distance,
    is_within_road_distance,
)


def test_acceptable_slope():
    assert is_slope_acceptable(10.0) is True


def test_unacceptable_slope():
    assert is_slope_acceptable(20.0) is False


def test_sufficient_solar_irradiance():
    assert has_sufficient_solar_irradiance(5.0) is True


def test_insufficient_solar_irradiance():
    assert has_sufficient_solar_irradiance(3.0) is False


def test_sufficient_wind_speed():
    assert has_sufficient_wind_speed(6.0) is True


def test_insufficient_wind_speed():
    assert has_sufficient_wind_speed(2.0) is False


def test_within_grid_distance():
    assert is_within_grid_distance(8.0) is True


def test_too_far_from_grid():
    assert is_within_grid_distance(15.0) is False


def test_within_road_distance():
    assert is_within_road_distance(3.0) is True


def test_too_far_from_road():
    assert is_within_road_distance(8.0) is False