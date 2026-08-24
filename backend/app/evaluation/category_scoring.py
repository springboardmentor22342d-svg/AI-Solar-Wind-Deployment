from backend.app.evaluation.normalization import (
    normalize_solar_irradiance,
    normalize_wind_speed,
    normalize_slope,
    normalize_distance_to_grid,
    normalize_distance_to_road
)


def calculate_renewable_resource_score(
    solar_irradiance: float,
    wind_speed: float
) -> float:
    """
    Calculate Renewable Resource Score.

    Solar Irradiance: 60%
    Wind Speed: 40%

    Returns:
        Score between 0 and 100.
    """

    solar_score = normalize_solar_irradiance(
        solar_irradiance
    )

    wind_score = normalize_wind_speed(
        wind_speed
    )

    score = (
        solar_score * 0.60
        + wind_score * 0.40
    )

    return round(score, 2)


def calculate_terrain_score(
    slope: float,
    elevation: float
) -> float:
    """
    Calculate Terrain Score.

    Slope: 70%
    Elevation: 30%

    Lower slope is better.
    Elevation is normalized between 0 and 3000 meters.

    Returns:
        Score between 0 and 100.
    """

    slope_score = normalize_slope(slope)

    elevation_score = (
        elevation / 3000
    ) * 100

    elevation_score = max(
        0,
        min(elevation_score, 100)
    )

    score = (
        slope_score * 0.70
        + elevation_score * 0.30
    )

    return round(score, 2)


def calculate_infrastructure_score(
    distance_to_road: float,
    distance_to_grid: float
) -> float:
    """
    Calculate Infrastructure Score.

    Grid Accessibility: 60%
    Road Accessibility: 40%

    Shorter distance is better.

    Returns:
        Score between 0 and 100.
    """

    grid_score = normalize_distance_to_grid(
        distance_to_grid
    )

    road_score = normalize_distance_to_road(
        distance_to_road
    )

    score = (
        grid_score * 0.60
        + road_score * 0.40
    )

    return round(score, 2)


def calculate_environmental_score(
    environmental_sensitivity: float
) -> float:
    """
    Calculate Environmental Score.

    Environmental sensitivity:
        0   = No sensitivity / best
        100 = Very high sensitivity / worst

    Lower environmental sensitivity
    produces a higher score.

    Returns:
        Score between 0 and 100.
    """

    score = 100 - environmental_sensitivity

    return round(
        max(0, min(score, 100)),
        2
    )


def calculate_economic_score(
    land_cost: float,
    estimated_roi: float
) -> float:
    """
    Calculate Economic Score.

    Land Cost:
        Lower is better.

    Estimated ROI:
        Higher is better.

    Assumptions:
        land_cost is represented as a 0-100 cost score.
        estimated_roi is represented as a 0-100 ROI score.

    Land Cost Weight: 40%
    ROI Weight: 60%

    Returns:
        Score between 0 and 100.
    """

    land_cost_score = 100 - land_cost

    land_cost_score = max(
        0,
        min(land_cost_score, 100)
    )

    roi_score = max(
        0,
        min(estimated_roi, 100)
    )

    score = (
        land_cost_score * 0.40
        + roi_score * 0.60
    )

    return round(score, 2)