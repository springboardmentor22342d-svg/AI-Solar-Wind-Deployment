from app.evaluation.weights import WEIGHTS

MAX_SOLAR_KWH = 8.0
MAX_WIND_MS = 12.0
MAX_SLOPE_DEG = 30.0
MAX_DIST_GRID_KM = 100.0
MAX_DIST_ROAD_KM = 50.0


def _norm(value: float, max_val: float, invert: bool = False) -> float:
    normalized = min(1.0, max(0.0, value / max_val))
    return (1.0 - normalized) if invert else normalized


def compute_weighted_score(features: dict, weights: dict = None) -> float:
    w = weights or WEIGHTS

    solar_score = _norm(features.get("solar_irradiance_kwh", 0), MAX_SOLAR_KWH)
    wind_score = _norm(features.get("wind_speed_ms", 0), MAX_WIND_MS)
    slope_score = _norm(features.get("slope_deg", MAX_SLOPE_DEG), MAX_SLOPE_DEG, invert=True)
    grid_score = _norm(features.get("dist_grid_km", MAX_DIST_GRID_KM), MAX_DIST_GRID_KM, invert=True)
    road_score = _norm(features.get("dist_road_km", MAX_DIST_ROAD_KM), MAX_DIST_ROAD_KM, invert=True)

    score = (
        solar_score * w.get("solar", 0)
        + wind_score * w.get("wind", 0)
        + slope_score * w.get("slope", 0)
        + grid_score * w.get("grid_distance", 0)
        + road_score * w.get("road_distance", 0)
    )

    return round(score * 100, 2)
