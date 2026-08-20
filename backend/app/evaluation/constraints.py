MAX_SLOPE_DEG = 15.0
MIN_SOLAR_IRRADIANCE = 3.5
MIN_WIND_SPEED = 3.0
MAX_DIST_GRID_KM = 50.0
MAX_DIST_ROAD_KM = 25.0


def check_slope(slope_deg: float) -> bool:
    return slope_deg <= MAX_SLOPE_DEG


def check_solar_irradiance(solar_kwh: float) -> bool:
    return solar_kwh >= MIN_SOLAR_IRRADIANCE


def check_wind_speed(wind_ms: float) -> bool:
    return wind_ms >= MIN_WIND_SPEED


def check_grid_distance(dist_km: float) -> bool:
    return dist_km <= MAX_DIST_GRID_KM


def check_road_distance(dist_km: float) -> bool:
    return dist_km <= MAX_DIST_ROAD_KM


def evaluate_all_constraints(features: dict) -> dict:
    return {
        "slope": check_slope(features.get("slope_deg", 999)),
        "solar_irradiance": check_solar_irradiance(features.get("solar_irradiance_kwh", 0)),
        "wind_speed": check_wind_speed(features.get("wind_speed_ms", 0)),
        "grid_distance": check_grid_distance(features.get("dist_grid_km", 999)),
        "road_distance": check_road_distance(features.get("dist_road_km", 999)),
    }
