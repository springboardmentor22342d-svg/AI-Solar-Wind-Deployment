from app.evaluation.constraints import evaluate_all_constraints
from app.evaluation.scorer import compute_weighted_score
from app.evaluation.recommendation import get_recommendation


def run_evaluation(features: dict) -> dict:
    constraint_results = evaluate_all_constraints(features)

    failed_constraints = [k for k, v in constraint_results.items() if not v]

    score = compute_weighted_score(features)

    if failed_constraints:
        score = min(score, 30.0)

    recommendation = get_recommendation(score)

    criteria_evaluation = {
        "solar_irradiance": {
            "value": features.get("solar_irradiance_kwh", 0),
            "status": "Pass" if constraint_results.get("solar_irradiance") else "Fail",
        },
        "wind_speed": {
            "value": features.get("wind_speed_ms", 0),
            "status": "Pass" if constraint_results.get("wind_speed") else "Fail",
        },
        "slope": {
            "value": features.get("slope_deg", 0),
            "status": "Pass" if constraint_results.get("slope") else "Fail",
        },
        "distance_to_grid": {
            "value": features.get("dist_grid_km", 0),
            "status": "Pass" if constraint_results.get("grid_distance") else "Fail",
        },
        "distance_to_road": {
            "value": features.get("dist_road_km", 0),
            "status": "Pass" if constraint_results.get("road_distance") else "Fail",
        },
    }

    return {
        "overall_score": score,
        "recommendation": recommendation,
        "criteria_evaluation": criteria_evaluation,
        "constraints": constraint_results,
        "failed_constraints": failed_constraints,
    }
