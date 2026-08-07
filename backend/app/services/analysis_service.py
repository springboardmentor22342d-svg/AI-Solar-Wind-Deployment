from app.evaluation.evaluator import evaluate_site
from app.scoring.site_scorer import calculate_site_score
from app.services.deployment_strategy import build_deployment_recommendation
from app.feasibility.feasibility_engine import assess_technical_feasibility
from app.services.energy_yield_service import estimate_solar_yield, estimate_wind_yield, estimate_hybrid_yield
from app.financial.financial_analysis_service import run_financial_analysis


class AnalysisService:
    def __init__(self, feature_builder, solar_prediction_service, wind_prediction_service):
        self.feature_builder = feature_builder
        self.solar_prediction_service = solar_prediction_service
        self.wind_prediction_service = wind_prediction_service

    def run_analysis(self, latitude: float, longitude: float, project_name: str = None,
                      installed_capacity_kw: float = 5000, tariff_per_kwh: float = 3.5) -> dict:
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

        feasibility = assess_technical_feasibility(features)

        wind_model_features = {**features, "wind_speed": features.get("wind_speed_100m")}
        deployment_type = deployment["deployment"]

        if deployment_type == "Solar":
            yield_result = estimate_solar_yield(
                installed_capacity_kw, features.get("solar_irradiance"),
                self.solar_prediction_service, features
            )
            annual_energy_yield = yield_result.get("annual_energy_kwh", 0)
        elif deployment_type == "Wind":
            yield_result = estimate_wind_yield(
                installed_capacity_kw, features.get("wind_speed_100m"),
                self.wind_prediction_service, wind_model_features
            )
            annual_energy_yield = yield_result.get("annual_energy_kwh", 0)
        elif deployment_type == "Hybrid":
            yield_result = estimate_hybrid_yield(
                installed_capacity_kw, features.get("solar_irradiance"), features.get("wind_speed_100m"),
                self.solar_prediction_service, self.wind_prediction_service, features
            )
            annual_energy_yield = yield_result.get("total_annual_energy_kwh", 0)
        else:
            yield_result = {"annual_energy_kwh": 0, "source": "not_applicable"}
            annual_energy_yield = 0

        financial_analysis = run_financial_analysis(
            annual_energy_yield, installed_capacity_kw, deployment_type, tariff_per_kwh
        )

        return {
            "project_name": project_name,
            "latitude": latitude,
            "longitude": longitude,
            "solar_features": solar_features,
            "wind_features": wind_features,
            "evaluation": evaluation_result,
            "site_score": site_score,
            "deployment_recommendation": deployment,
            "technical_feasibility": feasibility,
            "energy_yield": yield_result,
            "financial_analysis": financial_analysis,
            "raw_features": features,
        }