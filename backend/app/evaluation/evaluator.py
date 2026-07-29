from app.evaluation.constraints import run_all_constraints
from app.evaluation.recommendation import get_recommendation
from app.evaluation.scorer import compute_weighted_score


def evaluate_site(features: dict) -> dict:
    constraints = run_all_constraints(features)
    hard_constraints_passed = all(constraints.values())
    score = compute_weighted_score(features) if hard_constraints_passed else 0.0

    return {
        "suitability_score": score,
        "recommendation": get_recommendation(score),
        "hard_constraints_passed": hard_constraints_passed,
        "constraints": constraints,
    }
