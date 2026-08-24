"""
Recommendation generation for evaluated locations.

This module will convert suitability scores
into human-readable recommendations.
"""
"""
Recommendation logic for renewable energy site evaluation.
"""


def get_recommendation(score: float) -> str:
    """
    Convert a suitability score into a recommendation.

    Args:
        score:
            Suitability score from 0 to 100.

    Returns:
        Recommendation category.

    Recommendation rules:

        score >= 85
            Highly Suitable

        score >= 70
            Suitable

        score >= 50
            Moderately Suitable

        score < 50
            Not Recommended
    """

    if score >= 85:
        return "Highly Suitable"

    if score >= 70:
        return "Suitable"

    if score >= 50:
        return "Moderately Suitable"

    return "Not Recommended"