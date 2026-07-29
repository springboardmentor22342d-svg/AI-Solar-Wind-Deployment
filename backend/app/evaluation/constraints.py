"""
Hard constraint checks — a site failing any of these is flagged as
unsuitable regardless of its weighted score. Threshold values are
kept as named constants (not hardcoded inline) so they can be tuned
in one place.
"""

MAX_SLOPE_DEGREES = 15.0
MIN_SOLAR_IRRADIANCE_GHI = 4.0          # kWh/m²/day
MIN_WIND_SPEED_MS = 3.0                  # m/s (matches turbine cut-in speed)
MAX_DISTANCE_TO_SETTLEMENT_KM = 50.0     # proxy for grid + road distance


def check_slope(slope: float) -> bool:
    if slope is None:
        return False
    return slope <= MAX_SLOPE_DEGREES


def check_solar_irradiance(solar_irradiance: float) -> bool:
    if solar_irradiance is None:
        return False
    return solar_irradiance >= MIN_SOLAR_IRRADIANCE_GHI


def check_wind_speed(wind_speed: float) -> bool:
    if wind_speed is None:
        return False
    return wind_speed >= MIN_WIND_SPEED_MS


def check_distance_to_grid(distance_to_grid_km: float) -> bool:
    if distance_to_grid_km is None:
        return False
    return distance_to_grid_km <= MAX_DISTANCE_TO_SETTLEMENT_KM


def check_distance_to_road(distance_to_road_km: float) -> bool:
    if distance_to_road_km is None:
        return False
    return distance_to_road_km <= MAX_DISTANCE_TO_SETTLEMENT_KM

def run_all_constraints(features: dict) -> dict:
    return {
        "slope_ok": check_slope(features.get("slope")),
        "solar_irradiance_ok": check_solar_irradiance(features.get("solar_irradiance")),
        "wind_speed_ok": check_wind_speed(features.get("wind_speed")),
        "distance_to_grid_ok": check_distance_to_grid(features.get("distance_to_grid_km")),
        "distance_to_road_ok": check_distance_to_road(features.get("distance_to_road_km")),
    }