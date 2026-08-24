"""
Feature weights used during suitability evaluation.

This module will define the importance of each feature
in the final suitability score.
"""
"""
Weights used for suitability scoring.
"""

FEATURE_WEIGHTS = {
    "solar_irradiance": 0.35,
    "wind_speed": 0.25,
    "slope": 0.15,
    "distance_to_grid": 0.15,
    "distance_to_road": 0.10,
}