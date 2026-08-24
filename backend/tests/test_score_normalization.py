from backend.app.evaluation.normalization import (
    normalize_solar_irradiance,
    normalize_wind_speed,
    normalize_slope,
    normalize_distance_to_grid,
    normalize_distance_to_road
)


def test_solar_normalization():

    assert normalize_solar_irradiance(2) == 0
    assert normalize_solar_irradiance(8) == 100


def test_wind_normalization():

    assert normalize_wind_speed(2) == 0
    assert normalize_wind_speed(10) == 100


def test_slope_normalization():

    assert normalize_slope(0) == 100
    assert normalize_slope(30) == 0


def test_grid_distance_normalization():

    assert normalize_distance_to_grid(0) == 100
    assert normalize_distance_to_grid(50) == 0


def test_road_distance_normalization():

    assert normalize_distance_to_road(0) == 100
    assert normalize_distance_to_road(20) == 0