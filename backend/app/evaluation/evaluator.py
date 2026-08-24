"""
Main evaluation coordinator.

This module will combine constraints, weights,
scoring, and recommendations into one evaluation workflow.
"""
"""
Main evaluation service.

This module orchestrates:

1. Constraint checking
2. Weighted scoring
3. Recommendation generation
4. Explanation of failed constraints
"""

from typing import Any, Dict, List

from backend.app.evaluation.constraints import (
    is_slope_acceptable,
    has_sufficient_solar_irradiance,
    has_sufficient_wind_speed,
    is_within_grid_distance,
    is_within_road_distance,
)

from backend.app.evaluation.scorer import (
    calculate_weighted_score,
)

from backend.app.evaluation.recommendation import (
    get_recommendation,
)


class EvaluationService:
    """
    Coordinates the complete site evaluation workflow.
    """

    def evaluate(
        self,
        features: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Evaluate a location using its feature values.

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
            Structured evaluation result.

            Example:

            {
                "constraints_satisfied": True,
                "overall_score": 75.5,
                "recommendation": "Suitable",
                "failed_constraints": []
            }
        """

        failed_constraints: List[str] = []

        # -----------------------------
        # 1. Constraint Checking
        # -----------------------------

        if not is_slope_acceptable(
            features["slope"]
        ):
            failed_constraints.append(
                "Slope exceeds the maximum allowable limit."
            )

        if not has_sufficient_solar_irradiance(
            features["solar_irradiance"]
        ):
            failed_constraints.append(
                "Solar irradiance is below the minimum threshold."
            )

        if not has_sufficient_wind_speed(
            features["wind_speed"]
        ):
            failed_constraints.append(
                "Wind speed is below the minimum threshold."
            )

        if not is_within_grid_distance(
            features["distance_to_grid"]
        ):
            failed_constraints.append(
                "Location is too far from the electrical grid."
            )

        if not is_within_road_distance(
            features["distance_to_road"]
        ):
            failed_constraints.append(
                "Location is too far from a road."
            )

        # -----------------------------
        # 2. Weighted Score
        # -----------------------------

        overall_score = calculate_weighted_score(
            features
        )

        # -----------------------------
        # 3. Recommendation
        # -----------------------------

        recommendation = get_recommendation(
            overall_score
        )

        # -----------------------------
        # 4. Final Result
        # -----------------------------

        return {
            "constraints_satisfied": (
                len(failed_constraints) == 0
            ),
            "overall_score": overall_score,
            "recommendation": recommendation,
            "failed_constraints": failed_constraints,
        }