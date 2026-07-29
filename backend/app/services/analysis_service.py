"""
The unified analysis pipeline — orchestrates the full workflow:
    Site Details -> Feature Retrieval -> Evaluation -> Scoring -> Deployment Recommendation

Calls FeatureBuilder.build() exactly ONCE per request, then reuses
the result across all downstream steps, avoiding duplicate network
calls and raster reads (see dataset_summary.md, Task 5 refactor note).
"""

from app.evaluation.evaluator import evaluate_site
from app.scoring.site_scorer import calculate_site_score
from app.services.deployment_strategy import build_deployment_recommendation


class AnalysisService:
    def __init__(self, feature_builder):
        self.feature_builder = feature_builder

    def run_analysis(self, latitude: float, longitude: float, project_name: str = None) -> dict:
        # Step 1: Retrieve ALL features once (solar, wind, terrain, infra, land-use, climate)
        features = self.feature_builder.build(latitude, longitude)

        # Step 2: Extract solar/wind subsets from the already-computed features
        # (no duplicate calls — just reading keys from the existing result)
        solar_features = {
            "solar_irradiance": features.get("solar_irradiance"),
            "solar_irradiance_ghi": features.get("solar_irradiance_ghi"),
            "solar_irradiance_gti": features.get("solar_irradiance_gti"),
            "optimum_tilt_angle": features.get("optimum_tilt_angle"),
        }
        wind_features = {
            "wind_speed_100m": features.get("wind_speed_100m"),
            "power_density_100m": features.get("power_density_100m"),
        }

        # Step 3: Evaluate the site (constraints + suitability score)
        evaluation_input = {
            "solar_irradiance": features.get("solar_irradiance"),
            "wind_speed": features.get("wind_speed_100m"),
            "slope": features.get("slope"),
            "distance_to_grid_km": features.get("distance_to_grid_km"),
            "distance_to_road_km": features.get("distance_to_road_km"),
            "forest_pct": features.get("forest_pct"),
            "culturable_wasteland_pct": features.get("culturable_wasteland_pct"),
        }
        evaluation_result = evaluate_site(evaluation_input)

        # Step 4: Calculate the composite site score
        site_score = calculate_site_score(features)

        # Step 5: Generate the deployment recommendation
        deployment = build_deployment_recommendation(
            features.get("solar_irradiance"), features.get("wind_speed_100m")
        )

        # Step 6: Consolidate everything into one response
        return {
            "project_name": project_name,
            "latitude": latitude,
            "longitude": longitude,
            "solar_features": solar_features,
            "wind_features": wind_features,
            "evaluation": evaluation_result,
            "site_score": site_score,
            "deployment_recommendation": deployment,
            "raw_features": features,
        }