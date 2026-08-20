"""
Orchestrates the full workflow: Feature Store cache check -> site
validity check -> feature retrieval -> evaluation -> scoring ->
deployment recommendation -> technical feasibility -> energy yield
-> financial analysis.
"""

from app.evaluation.evaluator import evaluate_site
from app.evaluation.site_validity import check_site_validity
from app.scoring.site_scorer import calculate_site_score
from app.services.deployment_strategy import build_deployment_recommendation
from app.services.solar_assessment import classify_solar_site
from app.services.wind_assessment import calculate_wind_class
from app.feasibility.feasibility_engine import assess_technical_feasibility
from app.services.energy_yield_service import (
    estimate_solar_yield, estimate_wind_yield, estimate_hybrid_yield, rate_energy_yield,
)
from app.financial.financial_analysis_service import run_financial_analysis
from app.services.feature_store_service import FeatureStoreService
from app.schemas.feature import FeatureCreate
from app.evaluation.known_sites import check_nearby_known_installations


class AnalysisService:
    def __init__(self, feature_builder, solar_prediction_service, wind_prediction_service,
                 land_mask_client, feature_store_service):
        self.feature_builder = feature_builder
        self.solar_prediction_service = solar_prediction_service
        self.wind_prediction_service = wind_prediction_service
        self.land_mask_client = land_mask_client
        self.feature_store_service = feature_store_service

    def run_analysis(self, latitude: float, longitude: float, project_name: str = None,
                      installed_capacity_kw: float = 5000, tariff_per_kwh: float = 3.5) -> dict:

        cached = self.feature_store_service.find_by_coordinates(latitude, longitude)

        if cached:
            features = {
                "latitude": cached.latitude, "longitude": cached.longitude,
                "solar_irradiance": cached.solar_irradiance, "wind_speed_100m": cached.wind_speed,
                "temperature": cached.temperature, "humidity": cached.humidity,
                "elevation": cached.elevation, "slope": cached.slope,
                "solar_irradiance_gti": cached.solar_irradiance_gti,
                "optimum_tilt_angle": cached.optimum_tilt_angle,
                "power_density_100m": cached.power_density_100m,
                "nearby_settlement_count": cached.nearby_settlement_count,
                "distance_to_nearest_settlement_km": cached.distance_to_nearest_settlement_km,
                "nearest_settlement_name": cached.nearest_settlement_name,
                "forest_pct": cached.forest_pct, "net_area_sown_pct": cached.net_area_sown_pct,
                "fallow_land_pct": cached.fallow_land_pct, "culturable_wasteland_pct": cached.culturable_wasteland_pct,
                "distance_to_road_km": cached.distance_to_road_km, "distance_to_grid_km": cached.distance_to_grid_km,
            }
            data_source = "cache"
        else:
            features = self.feature_builder.build(latitude, longitude)
            data_source = "computed_live"

            try:
                self.feature_store_service.save(FeatureCreate(
                    latitude=latitude, longitude=longitude,
                    solar_irradiance=features.get("solar_irradiance"),
                    wind_speed=features.get("wind_speed_100m"),
                    temperature=features.get("temperature"), humidity=features.get("humidity"),
                    elevation=features.get("elevation"), slope=features.get("slope"),
                    solar_irradiance_gti=features.get("solar_irradiance_gti"),
                    optimum_tilt_angle=features.get("optimum_tilt_angle"),
                    power_density_100m=features.get("power_density_100m"),
                    nearby_settlement_count=features.get("nearby_settlement_count"),
                    distance_to_nearest_settlement_km=features.get("distance_to_nearest_settlement_km"),
                    nearest_settlement_name=features.get("nearest_settlement_name"),
                    forest_pct=features.get("forest_pct"), net_area_sown_pct=features.get("net_area_sown_pct"),
                    fallow_land_pct=features.get("fallow_land_pct"), culturable_wasteland_pct=features.get("culturable_wasteland_pct"),
                    distance_to_road_km=features.get("distance_to_road_km"), distance_to_grid_km=features.get("distance_to_grid_km"),
                ))
            except Exception:
                pass

        validity = check_site_validity(features, latitude, longitude, self.land_mask_client)
        if not validity["is_valid"]:
            return {
                "project_name": project_name, "latitude": latitude, "longitude": longitude,
                "site_valid": False, "validity_reasons": validity["reasons"],
                "message": "This location is not suitable for renewable energy analysis. See validity_reasons for details.",
            }

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

        solar_rating = classify_solar_site(features.get("solar_irradiance"))
        wind_rating = calculate_wind_class(features.get("wind_speed_100m"))

        feasibility = assess_technical_feasibility(features)

        nearby_installation = check_nearby_known_installations(latitude, longitude)

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
                self.solar_prediction_service, self.wind_prediction_service, wind_model_features
            )
            annual_energy_yield = yield_result.get("total_annual_energy_kwh", 0)
        else:
            yield_result = {"annual_energy_kwh": 0, "source": "not_applicable"}
            annual_energy_yield = 0

        yield_rating = rate_energy_yield(annual_energy_yield, deployment_type)

        financial_analysis = run_financial_analysis(
            annual_energy_yield, installed_capacity_kw, deployment_type, tariff_per_kwh
        )

        return {
            "project_name": project_name,
            "latitude": latitude,
            "longitude": longitude,
            "site_valid": True,
            "data_source": data_source,
            "site_suitability": evaluation_result,
            "recommended_deployment": deployment,
            "technical_feasibility": feasibility,
            "energy_yield": yield_result,
            "energy_yield_rating": yield_rating,
            "financial_metrics": financial_analysis,
            "recommendation_reason": deployment.get("reason", ""),
            "solar_rating": solar_rating,
            "wind_rating": wind_rating,
            "analysis_basis": deployment_type,
            "raw_features": features,
        }