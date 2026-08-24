from typing import Dict, Any


class FeasibilityEngine:
    """
    Technical feasibility engine.

    Evaluates whether a renewable-energy site
    satisfies technical requirements.
    """

    def __init__(
        self,
        min_solar_irradiance: float = 4.0,
        min_wind_speed: float = 4.0,
        max_slope: float = 15.0,
        max_grid_distance: float = 20.0,
        max_road_distance: float = 10.0,
    ):
        self.min_solar_irradiance = min_solar_irradiance
        self.min_wind_speed = min_wind_speed
        self.max_slope = max_slope
        self.max_grid_distance = max_grid_distance
        self.max_road_distance = max_road_distance

    def check_hard_constraints(
        self,
        features: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Check mandatory technical constraints.
        """

        failed_constraints = []

        if features["solar_irradiance"] < self.min_solar_irradiance:
            failed_constraints.append(
                "Solar irradiance is below the minimum threshold."
            )

        if features["wind_speed"] < self.min_wind_speed:
            failed_constraints.append(
                "Wind speed is below the minimum threshold."
            )

        if features["slope"] > self.max_slope:
            failed_constraints.append(
                "Site slope exceeds the maximum allowed limit."
            )

        if features["distance_to_grid"] > self.max_grid_distance:
            failed_constraints.append(
                "Site is too far from the electrical grid."
            )

        if features["distance_to_road"] > self.max_road_distance:
            failed_constraints.append(
                "Site is too far from a road."
            )

        return {
            "feasible": len(failed_constraints) == 0,
            "failed_constraints": failed_constraints
        }

    def calculate_soft_score(
        self,
        features: Dict[str, float]
    ) -> float:
        """
        Calculate a simple technical suitability score.
        """

        solar_score = min(
            features["solar_irradiance"] / 6.0 * 100,
            100
        )

        wind_score = min(
            features["wind_speed"] / 8.0 * 100,
            100
        )

        slope_score = max(
            0,
            100 - (features["slope"] / self.max_slope * 100)
        )

        grid_score = max(
            0,
            100 - (
                features["distance_to_grid"]
                / self.max_grid_distance * 100
            )
        )

        road_score = max(
            0,
            100 - (
                features["distance_to_road"]
                / self.max_road_distance * 100
            )
        )

        score = (
            0.35 * solar_score
            + 0.25 * wind_score
            + 0.15 * slope_score
            + 0.15 * grid_score
            + 0.10 * road_score
        )

        return round(score, 2)

    def evaluate(
        self,
        features: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Perform complete technical feasibility evaluation.
        """

        hard_constraints = self.check_hard_constraints(
            features
        )

        score = self.calculate_soft_score(
            features
        )

        if not hard_constraints["feasible"]:
            decision = "Not Feasible"
        elif score >= 85:
            decision = "Highly Feasible"
        elif score >= 70:
            decision = "Feasible"
        elif score >= 50:
            decision = "Moderately Feasible"
        else:
            decision = "Not Feasible"

        return {
            "technically_feasible": hard_constraints["feasible"],
            "hard_constraints": hard_constraints,
            "soft_score": score,
            "decision": decision
        }