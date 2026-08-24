"""
Scoring logic for renewable energy site evaluation.

This module will calculate suitability scores
from environmental, geographic, and infrastructure features.
"""
"""
Weighted scoring logic for renewable energy site evaluation.
"""

from typing import Dict

from backend.app.evaluation.weights import FEATURE_WEIGHTS


def calculate_weighted_score(
    features: Dict[str, float]
) -> float:
    """
    Calculate a weighted suitability score.

    Args:
        features:
            Dictionary containing feature values.

            Example:

            {
                "solar_irradiance": 5.8,
                "wind_speed": 6.2,
                "slope": 2.1,
                "distance_to_grid": 4.0,
                "distance_to_road": 2.0
            }

    Returns:
        Weighted suitability score as a float.

    Raises:
        KeyError:
            If a required feature is missing.
    """

    score = 0.0

    for feature_name, weight in FEATURE_WEIGHTS.items():

        if feature_name not in features:
            raise KeyError(
                f"Missing required feature: {feature_name}"
            )

        score += features[feature_name] * weight

    return score