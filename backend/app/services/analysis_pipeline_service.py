from app.spatial.spatial_service import SpatialAnalysisService

from app.services.evaluation_service import EvaluationService
from app.services.overall_scoring import OverallScoringService
from app.services.deployment_strategy import DeploymentStrategyService
from app.services.energy_estimation_service import EnergyEstimationService
from app.services.deployment_plan_service import DeploymentPlanService

from app.services.solar_assessment import SolarAssessmentService
from app.services.wind_assessment import WindAssessmentService
from app.financial.financial_analysis_service import FinancialAnalysisService
from app.feasibility.feasibility_engine import FeasibilityEngine


class AnalysisPipelineService:

    def __init__(self):
        self.spatial = SpatialAnalysisService()
        self.evaluation = EvaluationService()
        self.scoring = OverallScoringService()
        self.deployment = DeploymentStrategyService()
        self.energy = EnergyEstimationService()
        self.plan = DeploymentPlanService()
        self.solar = SolarAssessmentService()
        self.wind = WindAssessmentService()
        self.financial = FinancialAnalysisService()
        self.feasibility = FeasibilityEngine()

        try:
            from app.ml.model_inference import ModelInference
            from app.ml.feature_importance import FeatureImportance
            self.ml_inference = ModelInference()
            self.feature_importance = FeatureImportance()
        except Exception as e:
            print(f"ML components initialization note: {e}")
            self.ml_inference = None
            self.feature_importance = None

    def analyze_site(
        self,
        latitude: float,
        longitude: float,
    ):
        # -------------------------------------------------
        # STEP 1 : Generate Feature Vector & Ocean Check
        # -------------------------------------------------
        feature_vector = self.spatial.suitability_pipeline(
            latitude,
            longitude,
        )
        is_ocean = feature_vector.get("is_ocean", False)

        # -------------------------------------------------
        # STEP 2 : Technical Feasibility & Constraints
        # -------------------------------------------------
        feasibility_result = self.feasibility.evaluate(
            feature_vector
        )

        # -------------------------------------------------
        # STEP 3 : Overall Scoring
        # -------------------------------------------------
        scoring = self.scoring.calculate_from_features(
            feature_vector
        )
        if is_ocean:
            scoring["overall_suitability_score"] = 0.0
            scoring["overall_score"] = 0.0
            scoring["suitability_category"] = "Unfeasible (Ocean)"

        # -------------------------------------------------
        # STEP 4 : Solar & Wind Assessment
        # -------------------------------------------------
        solar = self.solar.classify_solar_site(
            feature_vector["solar_irradiance"]
        )
        wind = self.wind.classify_wind_site(
            feature_vector["wind_speed"]
        )

        feature_vector["solar_capacity_factor"] = solar["capacity_factor"] if not is_ocean else 0
        feature_vector["wind_capacity_factor"] = wind["capacity_factor"] if not is_ocean else 0
        feature_vector["resource_score"] = scoring["resource_score"] if not is_ocean else 0

        # -------------------------------------------------
        # STEP 5 : Deployment Recommendation
        # -------------------------------------------------
        deployment = self.deployment.recommend_from_features(
            feature_vector
        )
        feature_vector["deployment"] = deployment["recommendation"]

        # -------------------------------------------------
        # STEP 6 : Deployment Planning
        # -------------------------------------------------
        if is_ocean:
            plan = {
                "recommended_technology": "Unfeasible",
                "recommended_capacity_kw": 0,
                "expansion_status": "Not Feasible",
                "optimization_remarks": "Site is in open ocean/sea water body.",
            }
        else:
            plan = self.plan.generate_plan_from_features(
                feature_vector
            )
        feature_vector["installed_capacity"] = plan["recommended_capacity_kw"]

        # -------------------------------------------------
        # STEP 7 : Energy Estimation
        # -------------------------------------------------
        if is_ocean:
            energy = {
                "deployment_type": "Unfeasible",
                "installed_capacity_kw": 0,
                "annual_solar_energy_kwh": 0,
                "annual_wind_energy_kwh": 0,
                "total_annual_energy_kwh": 0,
            }
        else:
            energy = self.energy.estimate_from_features(
                feature_vector
            )

        # -------------------------------------------------
        # STEP 8 : Financial Analysis
        # -------------------------------------------------
        if is_ocean or plan["recommended_capacity_kw"] <= 0:
            financial = {
                "annual_revenue": 0.0,
                "estimated_project_cost": 0.0,
                "payback_period": "N/A",
                "roi": 0.0,
            }
        else:
            financial = self.financial.analyze(
                annual_energy_yield=energy["total_annual_energy_kwh"],
                electricity_tariff=feature_vector.get("electricity_tariff", 0.12),
                installed_capacity=plan["recommended_capacity_kw"],
                cost_per_kw=feature_vector.get("cost_per_kw", 1100.0),
                installation_percentage=feature_vector.get("installation_percentage", 15.0)
            )

        # -------------------------------------------------
        # STEP 9 : Evaluation
        # -------------------------------------------------
        evaluation = self.evaluation.evaluate_features(
            feature_vector
        )

        # -------------------------------------------------
        # STEP 10 : ML Inference & Feature Importance
        # -------------------------------------------------
        ml_result = {
            "predicted_solar_irradiance": feature_vector["solar_irradiance"],
            "top_features": []
        }

        if self.ml_inference and not is_ocean:
            try:
                sample_features = [
                    6, 15, 166, 24,
                    feature_vector["temperature"],
                    feature_vector["humidity"],
                    feature_vector["wind_speed"]
                ]
                pred_val = self.ml_inference.predict(sample_features)
                ml_result["predicted_solar_irradiance"] = round(pred_val, 2)
            except Exception as e:
                print(f"ML inference warning: {e}")

        if self.feature_importance:
            try:
                rankings = self.feature_importance.get_feature_importance()
                ml_result["top_features"] = rankings[:3] if rankings else []
            except Exception as e:
                print(f"Feature importance warning: {e}")

        # -------------------------------------------------
        # STEP 11 : Consolidated Report
        # -------------------------------------------------
        return {
            "location": {
                "latitude": latitude,
                "longitude": longitude,
                "is_ocean": is_ocean,
            },
            "features": feature_vector,
            "evaluation": evaluation,
            "feasibility": feasibility_result,
            "site_score": scoring,
            "deployment": deployment,
            "deployment_plan": plan,
            "energy_estimation": energy,
            "financial": financial,
            "ml_analysis": ml_result
        }