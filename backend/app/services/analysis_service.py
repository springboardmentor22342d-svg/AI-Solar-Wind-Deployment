"""
Orchestrates the full workflow: feature retrieval -> evaluation ->
scoring -> deployment recommendation -> energy estimation.

Both solar and wind energy estimation use trained ML models
(Random Forest) instead of rule-based formulas, wherever features
are complete. Falls back to reporting unavailability (not a crash)
when required features are missing.
"""

from app.evaluation.evaluator import evaluate_site
from app.scoring.site_scorer import calculate_site_score
from app.services.deployment_strategy import build_deployment_recommendation


class AnalysisService:
    def __init__(self, feature_builder, solar_prediction_service, wind_prediction_service):
        self.feature_builder = feature_builder
        self.solar_prediction_service = solar_prediction_service
        self.wind_prediction_service = wind_prediction_service

    def run_analysis(self, latitude: float, longitude: float, project_name: str = None,
                      installed_capacity_kw: float = 5000) -> dict:
        features = self.feature_builder.build(latitude, longitude)

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

        site_score = calculate_site_score(features)

        deployment = build_deployment_recommendation(
            features.get("solar_irradiance"), features.get("wind_speed_100m")
        )

        # ML-based solar energy prediction
        ml_solar_prediction = self.solar_prediction_service.predict(features)

        # ML-based wind energy prediction (alias wind_speed_100m -> wind_speed for the model's schema)
        wind_model_features = {**features, "wind_speed": features.get("wind_speed_100m")}
        ml_wind_prediction = self.wind_prediction_service.predict(wind_model_features)

        energy_summary = {
            "estimated_annual_solar_energy_kwh": ml_solar_prediction.get("prediction_kwh_year"),
            "solar_prediction_source": "ml_model" if ml_solar_prediction.get("error") is None else "unavailable",
            "solar_prediction_error": ml_solar_prediction.get("error"),
            "estimated_annual_wind_energy_kwh": ml_wind_prediction.get("prediction_kwh_year"),
            "wind_prediction_source": "ml_model" if ml_wind_prediction.get("error") is None else "unavailable",
            "wind_prediction_error": ml_wind_prediction.get("error"),
        }

        return {
            "project_name": project_name,
            "latitude": latitude,
            "longitude": longitude,
            "solar_features": solar_features,
            "wind_features": wind_features,
            "evaluation": evaluation_result,
            "site_score": site_score,
            "deployment_recommendation": deployment,
            "energy_summary": energy_summary,
            "raw_features": features,
        }