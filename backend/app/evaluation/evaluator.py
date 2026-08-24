from app.evaluation.constraints import (
    check_solar,
    check_wind,
    check_slope,
    check_grid_distance,
    check_road_distance,
)

from app.evaluation.scorer import (
    calculate_score,
    renewable_resource_score,
    terrain_score,
    infrastructure_score,
    environmental_score,
    economic_score,
)

from app.evaluation.recommendation import recommend


class Evaluator:

    def evaluate(self, feature):

        # Check constraints
        constraints = {
            "solar": check_solar(feature["solar"]),
            "wind": check_wind(feature["wind"]),
            "slope": check_slope(feature["slope"]),
            "grid": check_grid_distance(feature["grid"]),
            "road": check_road_distance(feature["road"]),
        }

        # Calculate scores
        overall_score = calculate_score(feature)

        renewable = renewable_resource_score(feature)
        terrain = terrain_score(feature)
        infrastructure = infrastructure_score(feature)
        environmental = environmental_score(feature)
        economic = economic_score(feature)

        # Recommendation
        recommendation = recommend(overall_score)

        return {
            "site_id": feature["site_id"],
            "latitude": feature["latitude"],
            "longitude": feature["longitude"],

            "overall_score": overall_score,

            "category_scores": {
                "renewable_resources": renewable,
                "terrain": terrain,
                "infrastructure": infrastructure,
                "environmental": environmental,
                "economic": economic,
            },

            "recommendation": recommendation,

            "criteria_evaluation": {
                "solar_irradiance": {
                    "value": feature["solar"],
                    "status": "Pass" if constraints["solar"] else "Fail",
                },
                "wind_speed": {
                    "value": feature["wind"],
                    "status": "Pass" if constraints["wind"] else "Fail",
                },
                "slope": {
                    "value": feature["slope"],
                    "status": "Pass" if constraints["slope"] else "Fail",
                },
                "distance_to_grid": {
                    "value": feature["grid"],
                    "status": "Pass" if constraints["grid"] else "Fail",
                },
                "distance_to_road": {
                    "value": feature["road"],
                    "status": "Pass" if constraints["road"] else "Fail",
                },
            },

            "constraints": {
                "protected_area": False,
                "water_body": False,
            },

            "remarks": [
                "High solar potential.",
                "Good road accessibility.",
                "Suitable for renewable energy deployment.",
            ],
        }