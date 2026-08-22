"""
Capacity planning — estimates recommended installation capacity
based on available land area and deployment type.

By default, only a portion of available land is allocated to the
initial recommended capacity (see UTILIZATION_RATIO), leaving room
for future expansion — matching realistic phased development
practice rather than committing 100% of land immediately.
"""

from app.optimization.constraints import SOLAR_LAND_USE_HA_PER_MW, WIND_LAND_USE_HA_PER_MW

DEFAULT_UTILIZATION_RATIO = 0.6  # use 60% of available land initially


def recommend_capacity_mw(land_area_hectares: float, deployment_type: str,
                           hybrid_split: float = 0.5, utilization_ratio: float = DEFAULT_UTILIZATION_RATIO) -> dict:
    if land_area_hectares is None or land_area_hectares <= 0:
        return {"solar_mw": 0.0, "wind_mw": 0.0, "total_mw": 0.0}

    usable_land = land_area_hectares * utilization_ratio

    if deployment_type == "Solar":
        solar_mw = round(usable_land / SOLAR_LAND_USE_HA_PER_MW, 2)
        return {"solar_mw": solar_mw, "wind_mw": 0.0, "total_mw": solar_mw}

    elif deployment_type == "Wind":
        wind_mw = round(usable_land / WIND_LAND_USE_HA_PER_MW, 2)
        return {"solar_mw": 0.0, "wind_mw": wind_mw, "total_mw": wind_mw}

    elif deployment_type == "Hybrid":
        solar_land = usable_land * hybrid_split
        wind_land = usable_land * (1 - hybrid_split)
        solar_mw = round(solar_land / SOLAR_LAND_USE_HA_PER_MW, 2)
        wind_mw = round(wind_land / WIND_LAND_USE_HA_PER_MW, 2)
        return {"solar_mw": solar_mw, "wind_mw": wind_mw, "total_mw": round(solar_mw + wind_mw, 2)}

    return {"solar_mw": 0.0, "wind_mw": 0.0, "total_mw": 0.0}