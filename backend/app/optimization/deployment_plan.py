"""
Generates a full deployment plan, combining technology recommendation,
capacity planning, expansion feasibility, and remarks into one result.
"""

from app.services.deployment_strategy import build_deployment_recommendation
from app.optimization.capacity_planning import recommend_capacity_mw
from app.optimization.expansion_analysis import analyze_expansion_feasibility
from app.optimization.constraints import (
    SOLAR_LAND_USE_HA_PER_MW,
    WIND_LAND_USE_HA_PER_MW,
    check_grid_capacity_constraint,
)


def generate_deployment_plan(features: dict, land_area_hectares: float,
                              grid_capacity_limit_mw: float = None) -> dict:
    """
    Input:
        features: site feature dict (solar_irradiance, wind_speed_100m, etc.)
        land_area_hectares: total available land for this site
        grid_capacity_limit_mw: optional override of the default grid limit

    Output: structured deployment plan.
    """
    solar_irradiance = features.get("solar_irradiance")
    wind_speed = features.get("wind_speed_100m")

    recommendation = build_deployment_recommendation(solar_irradiance, wind_speed)
    deployment_type = recommendation["deployment"]

    if deployment_type == "Not Recommended":
        return {
            "recommended_technology": "None",
            "recommended_capacity_mw": 0.0,
            "expansion_status": "Not Expandable",
            "optimization_remarks": recommendation["reason"],
            "confidence": recommendation["confidence"],
        }

    capacity = recommend_capacity_mw(land_area_hectares, deployment_type)

    # Determine actual land used, for expansion analysis
    if deployment_type == "Solar":
        land_used = capacity["solar_mw"] * SOLAR_LAND_USE_HA_PER_MW
    elif deployment_type == "Wind":
        land_used = capacity["wind_mw"] * WIND_LAND_USE_HA_PER_MW
    else:  # Hybrid
        land_used = (capacity["solar_mw"] * SOLAR_LAND_USE_HA_PER_MW) + (capacity["wind_mw"] * WIND_LAND_USE_HA_PER_MW)

    expansion_status = analyze_expansion_feasibility(land_area_hectares, land_used)

    remarks = [recommendation["reason"]]

    if grid_capacity_limit_mw is not None:
        grid_ok = check_grid_capacity_constraint(capacity["total_mw"], grid_capacity_limit_mw)
        if not grid_ok:
            remarks.append(
                f"Recommended capacity ({capacity['total_mw']} MW) exceeds the specified "
                f"grid capacity limit ({grid_capacity_limit_mw} MW) — capacity may need to be reduced."
            )

    return {
        "recommended_technology": deployment_type,
        "recommended_capacity_mw": capacity,
        "expansion_status": expansion_status,
        "optimization_remarks": " ".join(remarks),
        "confidence": recommendation["confidence"],
    }