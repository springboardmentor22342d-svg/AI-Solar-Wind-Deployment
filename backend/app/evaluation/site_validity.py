"""
Physical plausibility checks — rejects locations that are physically
unsuitable for any renewable energy deployment: open water (via
Natural Earth land polygon mask), extreme elevation, or missing
resource data indicating uninhabited/inaccessible terrain.
"""

MAX_REASONABLE_ELEVATION_M = 5500
MIN_REASONABLE_ELEVATION_M = -50


def check_site_validity(features: dict, latitude: float, longitude: float, land_mask_client=None) -> dict:
    reasons = []

    if land_mask_client is not None:
        if not land_mask_client.is_on_land(latitude, longitude):
            reasons.append("Coordinate is located in open water (ocean or large lake), not viable for land-based renewable energy deployment.")

    elevation = features.get("elevation")
    if elevation is not None:
        if elevation > MAX_REASONABLE_ELEVATION_M:
            reasons.append(f"Elevation ({elevation}m) exceeds practical development limit ({MAX_REASONABLE_ELEVATION_M}m).")
        if elevation < MIN_REASONABLE_ELEVATION_M:
            reasons.append(f"Elevation ({elevation}m) is implausibly low.")

    if features.get("solar_irradiance") is None and features.get("wind_speed_100m") is None:
        reasons.append("No solar or wind resource data available for this coordinate.")

    if features.get("nearby_settlement_count") == 0 and features.get("distance_to_nearest_settlement_km", 0) > 100:
        reasons.append("No settlements within 100km — location may be uninhabited or inaccessible terrain.")

    return {"is_valid": len(reasons) == 0, "reasons": reasons if reasons else "None"}