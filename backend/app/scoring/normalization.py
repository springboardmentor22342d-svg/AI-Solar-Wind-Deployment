"""
Reusable normalization functions — convert raw values (different
units, different ranges) onto a common 0-100 scale so they can be
combined fairly. Ranges are based on realistic India-wide values
(see dataset_summary.md).
"""

SOLAR_MIN, SOLAR_MAX = 3.0, 7.0            # GHI, kWh/m²/day
WIND_MIN, WIND_MAX = 2.0, 9.0              # m/s @ 100m
SLOPE_MIN, SLOPE_MAX = 0.0, 20.0           # degrees (lower is better)
DISTANCE_MIN, DISTANCE_MAX = 0.0, 50.0     # km (lower is better)
ELEVATION_MIN, ELEVATION_MAX = 0.0, 2000.0 # meters (moderate is often best, see terrain scoring)
FOREST_MIN, FOREST_MAX = 0.0, 100.0        # % (lower is better)
WASTELAND_MIN, WASTELAND_MAX = 0.0, 50.0   # % (higher is better)


def _normalize(value: float, low: float, high: float, invert: bool = False) -> float:
    """Scales any value to 0-100. invert=True means lower raw values score higher."""
    if value is None:
        return 0.0
    clamped = max(low, min(high, value))
    score = (clamped - low) / (high - low) * 100
    return round(100 - score if invert else score, 2)


def normalize_solar_irradiance(value: float) -> float:
    return _normalize(value, SOLAR_MIN, SOLAR_MAX)


def normalize_wind_speed(value: float) -> float:
    return _normalize(value, WIND_MIN, WIND_MAX)


def normalize_slope(value: float) -> float:
    return _normalize(value, SLOPE_MIN, SLOPE_MAX, invert=True)


def normalize_distance_to_grid(value: float) -> float:
    """Proxy: uses settlement distance (no separate grid-distance data available)."""
    return _normalize(value, DISTANCE_MIN, DISTANCE_MAX, invert=True)


def normalize_distance_to_road(value: float) -> float:
    """Proxy: uses settlement distance (no separate road-distance data available)."""
    return _normalize(value, DISTANCE_MIN, DISTANCE_MAX, invert=True)