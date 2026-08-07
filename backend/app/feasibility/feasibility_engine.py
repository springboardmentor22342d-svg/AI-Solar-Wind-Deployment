"""
Technical Feasibility Engine — wraps the existing evaluation module
(hard constraints + weighted scoring) into the specific output format
required by this task: technical feasibility %, violation counts,
critical violations, and overall status.

Reuses app/evaluation/ rather than duplicating constraint/scoring
logic (see project_mapping_sheet.md refactor notes).
"""

from app.evaluation.evaluator import evaluate_site
from app.evaluation.constraints import (
    check_slope, check_solar_irradiance, check_wind_speed,
    check_distance_to_grid, check_distance_to_road,
)

# Constraints considered CRITICAL — failing these makes a site
# fundamentally unbuildable, regardless of other factors
CRITICAL_CONSTRAINTS = ["slope_ok", "distance_to_grid_ok"]


def assess_technical_feasibility(features: dict) -> dict:
    """
    Input: feature dictionary (from FeatureBuilder).
    Output:
        {
            "technical_feasibility_pct": float,
            "constraint_violations": int,
            "critical_violations": list[str] or "None",
            "overall_status": "Feasible" | "Not Feasible",
            "constraint_details": dict
        }
    """
    evaluation_input = {
        "solar_irradiance": features.get("solar_irradiance"),
        "wind_speed": features.get("wind_speed_100m"),
        "slope": features.get("slope"),
        "distance_to_grid_km": features.get("distance_to_grid_km"),
        "distance_to_road_km": features.get("distance_to_road_km"),
        "forest_pct": features.get("forest_pct"),
        "culturable_wasteland_pct": features.get("culturable_wasteland_pct"),
    }

    evaluation = evaluate_site(evaluation_input)
    constraints = evaluation["constraints"]

    failed = [name for name, passed in constraints.items() if not passed]
    critical_failed = [name for name in failed if name in CRITICAL_CONSTRAINTS]

    overall_status = "Not Feasible" if critical_failed else "Feasible"
    technical_feasibility_pct = evaluation["suitability_score"] if overall_status == "Feasible" else 0.0

    return {
        "technical_feasibility_pct": round(technical_feasibility_pct, 2),
        "constraint_violations": len(failed),
        "critical_violations": critical_failed if critical_failed else "None",
        "overall_status": overall_status,
        "constraint_details": constraints,
    }