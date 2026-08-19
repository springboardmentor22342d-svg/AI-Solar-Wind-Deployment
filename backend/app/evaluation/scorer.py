from app.evaluation.weights import *

class WeightedScorer:

    @staticmethod
    def calculate_score(features: dict):

        score = (

            features["solar_irradiance"] * SOLAR_WEIGHT +

            features["wind_speed"] * WIND_WEIGHT +

            features["slope"] * SLOPE_WEIGHT +

            (10 - features["distance_to_grid"]) * GRID_WEIGHT +

            (10 - features["distance_to_road"]) * ROAD_WEIGHT

        )

        return round(score * 10, 2)