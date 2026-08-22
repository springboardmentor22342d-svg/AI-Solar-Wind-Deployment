"""
Combines all category scores into a single Overall Site Suitability
Score, using the project's official weighting:
    Renewable Resource Availability: 35%
    Geographic Suitability:          25%
    Infrastructure Accessibility:    15%
    Environmental Impact:            15%
    Economic Feasibility:            10%
"""

from app.scoring.category_scores import (
    calculate_resource_score,
    calculate_terrain_score,
    calculate_infrastructure_score,
    calculate_environmental_score,
    calculate_economic_score,
)

WEIGHT_RESOURCE = 0.35
WEIGHT_TERRAIN = 0.25
WEIGHT_INFRASTRUCTURE = 0.15
WEIGHT_ENVIRONMENTAL = 0.15
WEIGHT_ECONOMIC = 0.10


def calculate_site_score(features: dict) -> dict:
    """
    Input: a feature dictionary (from FeatureBuilder or Feature Store).
    Output: individual category scores + overall weighted score,
    matching the required output format.
    """
    resource_score = calculate_resource_score(features)
    terrain_score = calculate_terrain_score(features)
    infrastructure_score = calculate_infrastructure_score(features)
    environmental_score = calculate_environmental_score(features)
    economic_score = calculate_economic_score(features)

    overall_score = (
        resource_score * WEIGHT_RESOURCE
        + terrain_score * WEIGHT_TERRAIN
        + infrastructure_score * WEIGHT_INFRASTRUCTURE
        + environmental_score * WEIGHT_ENVIRONMENTAL
        + economic_score * WEIGHT_ECONOMIC
    )

    return {
        "resource_score": resource_score,
        "terrain_score": terrain_score,
        "infrastructure_score": infrastructure_score,
        "environmental_score": environmental_score,
        "economic_score": economic_score,
        "overall_score": round(overall_score, 2),
    }