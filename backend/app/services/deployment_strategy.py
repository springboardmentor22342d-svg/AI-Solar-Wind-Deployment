

from backend.app.services.hybrid_recommendation import (
    recommend_hybrid_strategy
)


class DeploymentStrategyService:

    def recommend_deployment(
        self,
        solar_class: str,
        wind_class: str
    ) -> str:

        return recommend_hybrid_strategy(
            solar_class,
            wind_class
        )

    def generate_reason(
        self,
        solar_class: str,
        wind_class: str
    ) -> str:

        deployment = self.recommend_deployment(
            solar_class,
            wind_class
        )

        if deployment == "Hybrid":
            return (
                "High solar irradiance and consistently strong "
                "wind resource."
            )

        elif deployment == "Solar":
            return (
                "Strong solar irradiance makes solar deployment "
                "the most suitable option."
            )

        elif deployment == "Wind":
            return (
                "Strong wind resource makes wind deployment "
                "the most suitable option."
            )

        else:
            return (
                "Both solar and wind resources are insufficient "
                "for a strong deployment recommendation."
            )

    def confidence_score(
        self,
        solar_class: str,
        wind_class: str
    ) -> int:

        score_map = {
            "Poor": 25,
            "Moderate": 50,
            "Good": 75,
            "Excellent": 95
        }

        solar_score = score_map[solar_class]
        wind_score = score_map[wind_class]

        deployment = self.recommend_deployment(
            solar_class,
            wind_class
        )

        if deployment == "Hybrid":
            return round(
                (solar_score + wind_score) / 2
            )

        elif deployment == "Solar":
            return solar_score

        elif deployment == "Wind":
            return wind_score

        return 20

    def generate_recommendation(
        self,
        solar_class: str,
        wind_class: str
    ) -> dict:

        deployment = self.recommend_deployment(
            solar_class,
            wind_class
        )

        confidence = self.confidence_score(
            solar_class,
            wind_class
        )

        reason = self.generate_reason(
            solar_class,
            wind_class
        )

        return {
            "deployment": deployment,
            "confidence": confidence,
            "reason": reason
        }
"""
Deployment Recommendation Module

Decides whether a location is best suited for Solar, Wind, or Hybrid deployment.
Integrates trained Machine Learning inference model with rule-based fallback logic.
"""

from typing import Optional, Dict, Any


def recommend_deployment(
    solar_class: str,
    wind_class: str
) -> str:
    """
    Rule-based baseline strategy recommendation.
    """
    if solar_class == "Excellent" and wind_class == "Excellent":
        return "Hybrid"

    if solar_class == "Excellent":
        return "Solar"

    if wind_class == "Excellent":
        return "Wind"

    if solar_class == "Good" and wind_class == "Good":
        return "Hybrid"

    if solar_class == "Good":
        return "Solar"

    if wind_class == "Good":
        return "Wind"

    return "Not Recommended"


def generate_reason(
    solar_class: str,
    wind_class: str
) -> str:
    """
    Explain recommendation.
    """
    deployment = recommend_deployment(solar_class, wind_class)
    reasons = {
        "Solar": "Solar irradiance is significantly stronger than wind resource.",
        "Wind": "Wind resource is stronger than available solar potential.",
        "Hybrid": "High solar irradiance and consistently strong wind resource.",
        "Not Recommended": "Neither solar nor wind resource is sufficient for deployment."
    }
    return reasons.get(deployment, "Resource potential evaluated for deployment.")


def confidence_score(
    solar_class: str,
    wind_class: str
) -> int:
    """
    Estimate recommendation confidence.
    """
    if solar_class == "Excellent" and wind_class == "Excellent":
        return 91
    if solar_class == "Excellent":
        return 88
    if wind_class == "Excellent":
        return 87
    if solar_class == "Good" or wind_class == "Good":
        return 75
    return 55


def recommend_strategy(
    solar_suitability: str,
    wind_suitability: str,
    solar_irradiance: Optional[float] = None,
    wind_speed: Optional[float] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None,
    extra_features: Optional[Dict[str, Any]] = None
) -> dict:
    """
    Produce deployment recommendation integrating ML model predictions with rule-based fallbacks.
    """
    def map_to_class(suitability: str) -> str:
        if suitability == "Excellent":
            return "Excellent"
        if suitability in ["Highly Suitable", "Moderately Suitable", "Good"]:
            return "Good"
        return "Poor"

    s_class = map_to_class(solar_suitability)
    w_class = map_to_class(wind_suitability)

    # 1. Fallback Rule-Based Result
    rule_dep = recommend_deployment(s_class, w_class)
    rule_conf = confidence_score(s_class, w_class)
    rule_reason = generate_reason(s_class, w_class)

    ml_prediction_data = None

    # 2. Try ML Model Inference Engine
    try:
        from app.ml.inference import ModelInferenceModule
        inference_module = ModelInferenceModule()

        # Deduce numeric values if not passed
        s_val = solar_irradiance if solar_irradiance is not None else (6.5 if s_class == "Excellent" else 5.2 if s_class == "Good" else 3.5)
        w_val = wind_speed if wind_speed is not None else (9.0 if w_class == "Excellent" else 6.5 if w_class == "Good" else 4.0)

        ml_res = inference_module.predict_deployment_strategy(
            solar_irradiance=s_val,
            wind_speed=w_val,
            latitude=latitude,
            longitude=longitude,
            extra_features=extra_features
        )

        dep = ml_res["deployment"]
        conf = ml_res["confidence"]
        reason = ml_res["reason"]
        ml_prediction_data = ml_res.get("ml_prediction")

    except Exception as e:
        dep = rule_dep
        conf = rule_conf
        reason = rule_reason

    return {
        "deployment": dep,
        "confidence": conf,
        "reason": reason,
        "ml_prediction": ml_prediction_data
    }
