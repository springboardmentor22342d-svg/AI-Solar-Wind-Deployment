"""
Category-wise scoring — combines related normalized values into one
score per evaluation category, matching the project's weighted
scoring model (see project PDF, page 7).
"""

from app.scoring.normalization import (
    normalize_solar_irradiance,
    normalize_wind_speed,
    normalize_slope,
    normalize_distance_to_grid,
    normalize_distance_to_road,
    _normalize,
    FOREST_MIN, FOREST_MAX,
    WASTELAND_MIN, WASTELAND_MAX,
)


def calculate_terrain_score(features: dict) -> float:
    """Geographic Suitability: primarily slope (elevation is contextual, not scored directly)."""
    return normalize_slope(features.get("slope"))


def calculate_infrastructure_score(features: dict) -> float:
    """Infrastructure Accessibility: grid + road proximity (real data)."""
    grid_score = normalize_distance_to_grid(features.get("distance_to_grid_km"))
    road_score = normalize_distance_to_road(features.get("distance_to_road_km"))
    return round((grid_score + road_score) / 2, 2)


def calculate_economic_score(features: dict) -> float:
    """Economic Feasibility: grid proximity as primary cost driver."""
    return normalize_distance_to_grid(features.get("distance_to_grid_km"))


def calculate_environmental_score(features: dict) -> float:
    """Environmental Impact: lower forest %, higher wasteland % is preferable."""
    forest_score = _normalize(features.get("forest_pct"), FOREST_MIN, FOREST_MAX, invert=True)
    wasteland_score = _normalize(features.get("culturable_wasteland_pct"), WASTELAND_MIN, WASTELAND_MAX)
    return round((forest_score + wasteland_score) / 2, 2)

def calculate_resource_score(features: dict) -> float:
    solar_score = normalize_solar_irradiance(features.get("solar_irradiance"))
    wind_score = normalize_wind_speed(features.get("wind_speed_100m"))  # fixed key name
    return round((solar_score + wind_score) / 2, 2)