"""
Hybrid deployment recommendation logic — combines solar and wind
classifications into a single deployment decision, with a confidence
score and human-readable reasoning.
"""

from app.services.solar_assessment import classify_solar_site
from app.services.wind_assessment import calculate_wind_class

RESOURCE_RANK = {"Poor": 0, "Moderate": 1, "Good": 2, "Excellent": 3, "Unknown": -1}


def recommend_deployment(solar_irradiance: float, wind_speed: float) -> str:
    solar_class = classify_solar_site(solar_irradiance)
    wind_class = calculate_wind_class(wind_speed)

    solar_rank = RESOURCE_RANK[solar_class]
    wind_rank = RESOURCE_RANK[wind_class]

    if solar_rank <= 0 and wind_rank <= 0:
        return "Not Recommended"
    if solar_rank >= 2 and wind_rank >= 2:
        return "Hybrid"
    if solar_rank > wind_rank:
        return "Solar"
    if wind_rank > solar_rank:
        return "Wind"
    return "Hybrid"  # equal ranks, both moderate-or-better


def generate_reason(solar_irradiance: float, wind_speed: float) -> str:
    solar_class = classify_solar_site(solar_irradiance)
    wind_class = calculate_wind_class(wind_speed)
    deployment = recommend_deployment(solar_irradiance, wind_speed)

    if deployment == "Hybrid":
        return f"{solar_class} solar irradiance and {wind_class.lower()} wind resource support a combined deployment."
    elif deployment == "Solar":
        return f"{solar_class} solar irradiance significantly outperforms {wind_class.lower()} wind resource at this site."
    elif deployment == "Wind":
        return f"{wind_class} wind resource significantly outperforms {solar_class.lower()} solar irradiance at this site."
    else:
        return f"Both solar irradiance ({solar_class.lower()}) and wind resource ({wind_class.lower()}) fall below viable thresholds."


def confidence_score(solar_irradiance: float, wind_speed: float) -> int:
    """
    Confidence reflects how CLEAR-CUT the decision is, regardless of
    whether the outcome is positive or negative:
      - Both resources clearly poor -> high confidence (clearly "no")
      - Both resources clearly excellent -> high confidence (clearly "yes")
      - Resources are close/moderate/mismatched -> lower confidence (ambiguous)
    """
    solar_class = classify_solar_site(solar_irradiance)
    wind_class = calculate_wind_class(wind_speed)
    solar_rank = RESOURCE_RANK[solar_class]
    wind_rank = RESOURCE_RANK[wind_class]

    if solar_rank == -1 or wind_rank == -1:
        return 0

    # How extreme is the average rank? (close to 0 or close to 3 = clear-cut)
    avg_rank = (solar_rank + wind_rank) / 2
    extremity = abs(avg_rank - 1.5) / 1.5  # 0 = middling, 1 = fully extreme

    # How much do solar and wind agree with each other?
    gap = abs(solar_rank - wind_rank)
    agreement = 1 - (gap / 3)  # 1 = perfect agreement, 0 = max disagreement

    confidence = 50 + (extremity * 30) + (agreement * 20)
    return round(min(100, confidence))


def build_deployment_recommendation(solar_irradiance: float, wind_speed: float) -> dict:
    """
    Combines everything into the final structured output.
    """
    return {
        "deployment": recommend_deployment(solar_irradiance, wind_speed),
        "confidence": confidence_score(solar_irradiance, wind_speed),
        "reason": generate_reason(solar_irradiance, wind_speed),
    }