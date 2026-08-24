"""
Constraint validation for renewable energy site evaluation.

This module will check whether a location violates
geographic, environmental, or infrastructure constraints.
"""

"""
Constraint validation for renewable energy site evaluation.

Each constraint function returns:

    True  → Constraint is satisfied
    False → Constraint is violated

Threshold values are defined as configurable constants.
"""

# -----------------------------
# Configurable Thresholds
# -----------------------------

MAX_SLOPE_DEGREES = 15.0

MIN_SOLAR_IRRADIANCE = 4.0

MIN_WIND_SPEED = 4.0

MAX_DISTANCE_TO_GRID_KM = 10.0

MAX_DISTANCE_TO_ROAD_KM = 5.0


# -----------------------------
# Constraint Functions
# -----------------------------

def is_slope_acceptable(slope: float) -> bool:
    """
    Check whether the slope is within the maximum allowed limit.

    Args:
        slope:
            Slope in degrees.

    Returns:
        True if slope is acceptable.
        False if slope exceeds the maximum threshold.
    """

    return slope <= MAX_SLOPE_DEGREES


def has_sufficient_solar_irradiance(
    solar_irradiance: float
) -> bool:
    """
    Check whether solar irradiance meets the minimum threshold.

    Args:
        solar_irradiance:
            Solar irradiance value.

    Returns:
        True if the minimum solar irradiance is met.
        False otherwise.
    """

    return solar_irradiance >= MIN_SOLAR_IRRADIANCE


def has_sufficient_wind_speed(
    wind_speed: float
) -> bool:
    """
    Check whether wind speed meets the minimum threshold.

    Args:
        wind_speed:
            Wind speed in meters per second.

    Returns:
        True if the minimum wind speed is met.
        False otherwise.
    """

    return wind_speed >= MIN_WIND_SPEED


def is_within_grid_distance(
    distance_to_grid: float
) -> bool:
    """
    Check whether the location is within the maximum
    allowable distance from the electrical grid.

    Args:
        distance_to_grid:
            Distance to grid in kilometers.

    Returns:
        True if within the allowed distance.
        False otherwise.
    """

    return distance_to_grid <= MAX_DISTANCE_TO_GRID_KM


def is_within_road_distance(
    distance_to_road: float
) -> bool:
    """
    Check whether the location is within the maximum
    allowable distance from a road.

    Args:
        distance_to_road:
            Distance to road in kilometers.

    Returns:
        True if within the allowed distance.
        False otherwise.
    """

    return distance_to_road <= MAX_DISTANCE_TO_ROAD_KM