"""
Weighted scoring logic. Each raw feature is first normalized to a
0-100 scale (since solar, wind, slope, and distance are all in
different units and ranges), then combined using the weights from
weights.py.

Normalization ranges are based on realistic values observed across
India (see dataset_summary.md for the underlying data ranges).
"""

from app.evaluation.weights import (
    WEIGHT_RESOURCE_AVAILABILITY,
    WEIGHT_GEOGRAPHIC_SUITABILITY,
    WEIGHT_INFRASTRUCTURE,
    WEIGHT_ENVIRONMENTAL_IMPACT,
    WEIGHT_ECONOMIC_FEASIBILITY,
    SOLAR_SUB_WEIGHT,
    WIND_SUB_WEIGHT,
)

# Realistic min/max ranges for normalization (India-wide)
SOLAR_MIN, SOLAR_MAX = 3.0, 7.0            # GHI, kWh/m²/day
WIND_MIN, WIND_MAX = 2.0, 9.0              # m/s @ 100m
SLOPE_MIN, SLOPE_MAX = 0.0, 20.0           # degrees (lower is better)
DISTANCE_MIN, DISTANCE_MAX = 0.0, 50.0     # km (lower is better)
FOREST_MIN, FOREST_MAX = 0.0, 100.0        # % (lower is better)
WASTELAND_MIN, WASTELAND_MAX = 0.0, 50.0   # % (higher is better)


def _normalize(value: float, low: float, high: float, invert: bool = False) -> float:
    """Scales a value to 0-100. If invert=True, lower raw values score higher."""
    if value is None:
        return 0.0
    clamped = max(low, min(high, value))
    score = (clamped - low) / (high - low) * 100
    return 100 - score if invert else score


def compute_resource_score(features: dict) -> float:
    solar_score = _normalize(features.get("solar_irradiance"), SOLAR_MIN, SOLAR_MAX)
    wind_score = _normalize(features.get("wind_speed"), WIND_MIN, WIND_MAX)
    return (solar_score * SOLAR_SUB_WEIGHT) + (wind_score * WIND_SUB_WEIGHT)


def compute_geographic_score(features: dict) -> float:
    return _normalize(features.get("slope"), SLOPE_MIN, SLOPE_MAX, invert=True)


def compute_infrastructure_score(features: dict) -> float:
    grid_score = _normalize(features.get("distance_to_grid_km"), DISTANCE_MIN, DISTANCE_MAX, invert=True)
    road_score = _normalize(features.get("distance_to_road_km"), DISTANCE_MIN, DISTANCE_MAX, invert=True)
    return (grid_score + road_score) / 2


def compute_economic_score(features: dict) -> float:
    return _normalize(features.get("distance_to_grid_km"), DISTANCE_MIN, DISTANCE_MAX, invert=True)


def compute_environmental_score(features: dict) -> float:
    forest_score = _normalize(features.get("forest_pct"), FOREST_MIN, FOREST_MAX, invert=True)
    wasteland_score = _normalize(features.get("culturable_wasteland_pct"), WASTELAND_MIN, WASTELAND_MAX)
    return (forest_score + wasteland_score) / 2



def compute_weighted_score(features: dict) -> float:
    """
    Combines all sub-scores into the final weighted suitability score (0-100).
    """
    resource = compute_resource_score(features) * WEIGHT_RESOURCE_AVAILABILITY
    geographic = compute_geographic_score(features) * WEIGHT_GEOGRAPHIC_SUITABILITY
    infrastructure = compute_infrastructure_score(features) * WEIGHT_INFRASTRUCTURE
    environmental = compute_environmental_score(features) * WEIGHT_ENVIRONMENTAL_IMPACT
    economic = compute_economic_score(features) * WEIGHT_ECONOMIC_FEASIBILITY

    total = resource + geographic + infrastructure + environmental + economic
    return round(total, 2)