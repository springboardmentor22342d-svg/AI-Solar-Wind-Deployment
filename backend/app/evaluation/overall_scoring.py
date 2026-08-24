from typing import Dict


DEFAULT_CATEGORY_WEIGHTS = {
    "renewable_resource": 0.35,
    "terrain": 0.15,
    "infrastructure": 0.20,
    "environmental": 0.15,
    "economic": 0.15
}


def calculate_overall_site_score(
    category_scores: Dict[str, float],
    weights: Dict[str, float] | None = None
) -> Dict:
    """
    Calculate final site suitability score.

    Returns:
    - Individual category scores
    - Overall score
    - Suitability classification
    """

    if weights is None:
        weights = DEFAULT_CATEGORY_WEIGHTS

    if set(category_scores.keys()) != set(weights.keys()):
        raise ValueError(
            "Category scores and weights must contain "
            "the same categories"
        )

    total_weight = sum(weights.values())

    if total_weight != 1:
        raise ValueError(
            "Category weights must sum to 1.0"
        )

    overall_score = sum(
        category_scores[category] * weights[category]
        for category in category_scores
    )

    overall_score = round(overall_score, 2)

    if overall_score >= 85:
        suitability = "Highly Suitable"

    elif overall_score >= 70:
        suitability = "Suitable"

    elif overall_score >= 50:
        suitability = "Moderately Suitable"

    else:
        suitability = "Not Recommended"

    return {
        "category_scores": category_scores,
        "overall_score": overall_score,
        "suitability": suitability
    }