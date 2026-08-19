from app.evaluation.constraints import evaluate_constraints

from app.evaluation.scorer import WeightedScorer

from app.evaluation.recommendation import RecommendationEngine


class Evaluator:

    @staticmethod
    def evaluate(site_id: int, features: dict):

        constraint_results = evaluate_constraints(features)

        score = WeightedScorer.calculate_score(features)

        recommendation = RecommendationEngine.generate(score)

        remarks = []

        if constraint_results["solar"]:
            remarks.append("High solar potential.")
        else:
            remarks.append("Low solar irradiance.")

        if constraint_results["wind"]:
            remarks.append("Good wind resource.")
        else:
            remarks.append("Poor wind resource.")

        if constraint_results["slope"]:
            remarks.append("Slope is suitable.")
        else:
            remarks.append("Terrain too steep.")

        if constraint_results["grid_distance"]:
            remarks.append("Close to grid.")
        else:
            remarks.append("Far from transmission grid.")

        if constraint_results["road_distance"]:
            remarks.append("Good road connectivity.")
        else:
            remarks.append("Poor road connectivity.")

        return {

            "site_id": site_id,

            "latitude": features["latitude"],

            "longitude": features["longitude"],

            "overall_score": score,

            "recommendation": recommendation,

            "criteria_evaluation": {

                "solar_irradiance": {

                    "value": features["solar_irradiance"],

                    "status": "Pass" if constraint_results["solar"] else "Fail"

                },

                "wind_speed": {

                    "value": features["wind_speed"],

                    "status": "Pass" if constraint_results["wind"] else "Fail"

                },

                "slope": {

                    "value": features["slope"],

                    "status": "Pass" if constraint_results["slope"] else "Fail"

                },

                "distance_to_grid": {

                    "value": features["distance_to_grid"],

                    "status": "Pass" if constraint_results["grid_distance"] else "Fail"

                },

                "distance_to_road": {

                    "value": features["distance_to_road"],

                    "status": "Pass" if constraint_results["road_distance"] else "Fail"

                }

            },

            "constraints": {

                "protected_area": False,

                "water_body": False

            },

            "remarks": remarks

        }