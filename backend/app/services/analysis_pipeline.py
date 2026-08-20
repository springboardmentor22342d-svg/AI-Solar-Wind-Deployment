from app.services.feature_engineering.feature_builder import FeatureBuilder
from app.evaluation.evaluator import run_evaluation
from app.services.deployment_strategy import recommend_deployment
from app.data_sources.time_series_loader import TimeSeriesDataLoader
from app.services.forecasting.feature_extractor import TemporalFeatureExtractor
from app.services.forecasting.solar_forecaster import SolarForecaster
from app.services.forecasting.wind_forecaster import WindForecaster
from app.services.forecasting.hybrid_forecaster import HybridForecaster
from app.services.ml_inference import ml_engine
from app.services.feasibility import evaluate_feasibility
from app.services.energy_estimation import estimate_annual_energy
from app.services.financial_analysis import generate_financial_metrics
import hashlib

class AnalysisPipeline:
    """
    A unified service that executes the complete analysis workflow for a given site.
    """
    
    def __init__(self):
        self.feature_builder = FeatureBuilder()
        self.time_series_loader = TimeSeriesDataLoader()
        self.solar_forecaster = SolarForecaster()
        self.wind_forecaster = WindForecaster()
        self.hybrid_forecaster = HybridForecaster()
        
    def execute_pipeline(self, latitude: float, longitude: float, site_name: str = None) -> dict:
        """
        Executes the full pipeline:
        1. Retrieve features
        2. Evaluate the site (score and constraints)
        3. Determine deployment recommendation
        4. Return consolidated response
        """
        
        # 1. Retrieve all features
        features = self.feature_builder.build_features(latitude, longitude)
        
        # Ensure 'wind_speed_ms' is present for the evaluator (use 50m as standard hub height)
        if "wind_speed_50m_ms" in features and features["wind_speed_50m_ms"] is not None:
            features["wind_speed_ms"] = features["wind_speed_50m_ms"]
        else:
            features["wind_speed_ms"] = 0.0

        # Also provide defaults if data sources fail
        if features.get("solar_irradiance_kwh") is None:
            features["solar_irradiance_kwh"] = 0.0
            
        if features.get("slope_deg") is None:
            features["slope_deg"] = 0.0
            
        if features.get("dist_grid_km") is None:
            features["dist_grid_km"] = 0.0
            
        if features.get("dist_road_km") is None:
            features["dist_road_km"] = 0.0

        # 2. Evaluate the site (constraints via rules, score via ML)
        evaluation_result = run_evaluation(features)
        ml_score, feature_importances = ml_engine.predict_suitability(features)
        
        # 3. Technical Feasibility
        feasibility_result = evaluate_feasibility(features)
        
        # 4. Generate deployment recommendation
        deployment_rec = recommend_deployment(
            solar_irradiance=features["solar_irradiance_kwh"],
            wind_speed=features["wind_speed_ms"]
        )
        
        # 5. Forecasting Integration
        forecast_data = []
        rec_tech = deployment_rec["deployment"]
        if rec_tech in ["Solar", "Wind", "Hybrid"]:
            # Load historical data
            historical_data = self.time_series_loader.load_historical_data(latitude, longitude, days_back=365)
            # Extract temporal features
            transformed_data = TemporalFeatureExtractor.transform_series(historical_data)
            
            # Forecast based on deployment recommendation
            if rec_tech == "Solar":
                forecast_data = self.solar_forecaster.forecast(transformed_data, days_ahead=30)
            elif rec_tech == "Wind":
                forecast_data = self.wind_forecaster.forecast(transformed_data, days_ahead=30)
            elif rec_tech == "Hybrid":
                forecast_data = self.hybrid_forecaster.forecast(transformed_data, days_ahead=30)
                
        # 6. Energy Yield & Financial Metrics
        # Synthesize capacity factors based on features
        solar_cf = min(100.0, (features["solar_irradiance_kwh"] / 8.0) * 25.0) # Approx
        wind_cf = min(100.0, (features["wind_speed_ms"] / 12.0) * 35.0) # Approx
        
        energy_yield = None
        financial_metrics = None
        
        if rec_tech in ["Solar", "Wind", "Hybrid"]:
            energy_yield = estimate_annual_energy(
                site_evaluation={"solar_capacity_factor": solar_cf, "wind_capacity_factor": wind_cf},
                deployment_type=rec_tech,
                capacity_mw=100.0 # Default assumption
            )
            
            financial_metrics = generate_financial_metrics(
                annual_energy_yield_mwh=energy_yield["total_energy_mwh"],
                installed_capacity_mw=100.0
            )

        # 7. Synthesize 5 Pillars & Geospatial Analytics
        # Resource Availability (Weight: 35%)
        solar_resource = min(100.0, (features["solar_irradiance_kwh"] / 7.0) * 100)
        wind_resource = min(100.0, (features["wind_speed_ms"] / 10.0) * 100)
        resource_score = (solar_resource * 0.6) + (wind_resource * 0.4) # Blend

        # Geographic Suitability (Weight: 25%)
        # Lower slope is better
        geo_score = max(0.0, 100.0 - (features["slope_deg"] * 5.0))

        # Infrastructure Access (Weight: 15%)
        grid_score = max(0.0, 100.0 - (features["dist_grid_km"] * 2.0))
        road_score = max(0.0, 100.0 - (features["dist_road_km"] * 5.0))
        infra_score = (grid_score * 0.7) + (road_score * 0.3)

        # Environmental Impact (Weight: 15%)
        env_score = 90.0 # Mocked high for typical non-restricted areas
        
        # Economic Feasibility (Weight: 10%)
        # Based on ROI (e.g. 10% ROI -> 100 score)
        econ_score = min(100.0, (financial_metrics["roi"] / 10.0) * 100) if financial_metrics else 50.0

        pillars = {
            "resource_availability": round(resource_score, 1),
            "geographic_suitability": round(geo_score, 1),
            "infrastructure_access": round(infra_score, 1),
            "environmental_impact": round(env_score, 1),
            "economic_feasibility": round(econ_score, 1)
        }

        # Geospatial Mocking
        mock_ndvi = 0.35 + (latitude % 10) * 0.02
        zoning = "Clear (Outside Forest Reserves)" if infra_score > 40 else "Restricted (Near Reserves)"
        
        geospatial = {
            "terrain_slope": round(features["slope_deg"], 1),
            "ndvi": round(mock_ndvi, 2),
            "zoning_status": zoning,
            "land_cover": features.get("land_cover_class", "Unknown").title()
        }

        # 8. Generate 12-Month Projection
        monthly_yields = []
        if energy_yield:
            # Simple seasonal distribution curve (Northern Hemisphere approximation)
            # Peaks in summer for solar, peaks in winter/spring for wind
            solar_curve = [0.06, 0.07, 0.09, 0.10, 0.11, 0.11, 0.11, 0.10, 0.09, 0.07, 0.05, 0.04]
            wind_curve = [0.10, 0.10, 0.11, 0.10, 0.08, 0.07, 0.06, 0.06, 0.07, 0.08, 0.08, 0.09]
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            
            # If Southern Hemisphere, shift solar by 6 months
            if latitude < 0:
                solar_curve = solar_curve[6:] + solar_curve[:6]
                
            for i, month in enumerate(months):
                monthly_yields.append({
                    "month": month,
                    "solar_gwh": round((energy_yield["solar_energy_mwh"] * solar_curve[i]) / 1000.0, 2),
                    "wind_gwh": round((energy_yield["wind_energy_mwh"] * wind_curve[i]) / 1000.0, 2)
                })

        # 9. Consolidate response
        site_id = hashlib.md5(f"{latitude}:{longitude}".encode()).hexdigest()[:8].upper()
        return {
            "site_id": f"SITE-{site_id}",
            "site_name": site_name,
            "latitude": latitude,
            "longitude": longitude,
            "features": features,
            "feature_importance": feature_importances,
            "evaluation": {
                "overall_score": round(ml_score, 2),
                "criteria_evaluation": evaluation_result["criteria_evaluation"],
                "constraints": evaluation_result["constraints"],
                "failed_constraints": evaluation_result["failed_constraints"]
            },
            "pillars": pillars,
            "geospatial": geospatial,
            "technical_feasibility": feasibility_result,
            "deployment": {
                "recommended_technology": deployment_rec["deployment"],
                "confidence": deployment_rec["confidence"],
                "reason": deployment_rec["reason"],
                "solar_class": deployment_rec["solar_class"],
                "wind_class": deployment_rec["wind_class"]
            },
            "energy_yield": energy_yield,
            "financial_metrics": financial_metrics,
            "forecast": forecast_data,
            "monthly_yields": monthly_yields
        }
