

from datetime import datetime

from backend.app.services.solar_assessment import SolarAssessmentService
from backend.app.data_sources.nasa_power import NasaPowerClient
from backend.app.data_sources.global_wind_atlas import GlobalWindAtlasClient
from backend.app.services.wind_assessment import classify_wind_site
from backend.app.evaluation.evaluator import EvaluationService
from backend.app.services.deployment_strategy import DeploymentStrategyService
from backend.app.inference.model_inference import ModelInference
from backend.app.feasibility.feasibility import FeasibilityEngine

from backend.app.energy_yield.energy_yield_service import EnergyYieldService
from backend.app.financial.financial_analysis import FinancialAnalysisService


class AnalysisPipeline:
    """
    Main analysis pipeline.

    Combines:
    - Solar assessment
    - Wind assessment
    - Site evaluation
    - Deployment recommendation
    - Machine learning prediction
    - Technical feasibility
    - Energy yield estimation
    - Financial analysis
    """

    def __init__(self):

        self.nasa_client = NasaPowerClient()
        self.wind_client = GlobalWindAtlasClient()

        self.solar_service = SolarAssessmentService()

        self.evaluation_service = EvaluationService()

        self.deployment_service = DeploymentStrategyService()

        # Load ML model once when the pipeline is created
        self.model_inference = ModelInference(
            "models/best_model.pkl"
        )

        self.feasibility_service = FeasibilityEngine()

        self.energy_yield_service = EnergyYieldService()

        self.financial_service = FinancialAnalysisService()

    # --------------------------------------------------
    # Get Site Features
    # --------------------------------------------------

    def get_site_features(
    self,
    latitude: float,
    longitude: float
    ):
  

        solar_data = self.nasa_client.fetch(
        latitude,
        longitude
      )

        if solar_data is None:
            raise RuntimeError(
            "Unable to retrieve NASA POWER solar data."
            )

        return {
        "latitude": latitude,
        "longitude": longitude,

        # Real NASA POWER data
        "temperature": solar_data["temperature"],
        "humidity": solar_data["humidity"],
        "solar_irradiance": solar_data["solar_irradiance"],

        # These still need real data sources later
        "wind_speed": 6.8,
        "elevation": 120,
        "slope": 4,
        "distance_to_grid": 6,
        "distance_to_road": 2
        }

    # --------------------------------------------------
    # Main Analysis
    # --------------------------------------------------

    def analyze(
        self,
        latitude: float,
        longitude: float
    ):
        """
        Execute the complete analysis pipeline.
        """

        # --------------------------------------------------
        # 1. Get environmental features
        # --------------------------------------------------

        features = self.get_site_features(
            latitude,
            longitude
        )

        # --------------------------------------------------
        # 2. Solar analysis
        # --------------------------------------------------

        solar_class = self.solar_service.classify_solar_site(
            features["solar_irradiance"]
        )

        # --------------------------------------------------
        # 3. Wind analysis
        # --------------------------------------------------

        wind_result = classify_wind_site(
            features["wind_speed"]
        )

        # --------------------------------------------------
        # 4. Site evaluation
        # --------------------------------------------------

        evaluation = self.evaluation_service.evaluate(
            features
        )

        # --------------------------------------------------
        # 5. Deployment recommendation
        # --------------------------------------------------

        deployment = self.deployment_service.recommend_deployment(
            solar_class,
            wind_result.get("wind_class")
        )

        # --------------------------------------------------
        # 6. Prepare ML prediction input
        # --------------------------------------------------

        today = datetime.now()

        model_features = {
            "temperature": features["temperature"],
            "humidity": features["humidity"],
            "wind_speed": features["wind_speed"],
            "solar_irradiance": features["solar_irradiance"],
            "year": today.year,
            "month": today.month,
            "day": today.day,
            "day_of_year": today.timetuple().tm_yday
        }

        # --------------------------------------------------
        # 7. Generate ML prediction
        # --------------------------------------------------

        prediction = self.model_inference.predict(
            model_features
        )

        # --------------------------------------------------
        # 8. Technical feasibility
        # --------------------------------------------------

        feasibility_result = self.feasibility_service.evaluate(
            features
        )

        # --------------------------------------------------
        # 9. Energy yield estimation
        # --------------------------------------------------

        # Example project capacity
        solar_capacity_mw = 10.0
        wind_capacity_mw = 10.0

        energy_yield = (
            self.energy_yield_service.estimate_hybrid_energy(
                solar_capacity_mw=solar_capacity_mw,
                wind_capacity_mw=wind_capacity_mw,
                solar_irradiance=features["solar_irradiance"],
                wind_speed=features["wind_speed"]
            )
        )
        annual_energy_mwh = energy_yield["total_annual_energy_mwh"]
        # --------------------------------------------------
        # 10. Financial Analysis
        # --------------------------------------------------

        annual_energy_mwh = (
            energy_yield["total_annual_energy_mwh"]
        )

        # Financial assumptions
        electricity_tariff = 5.0

        installed_capacity_mw = (
            solar_capacity_mw + wind_capacity_mw
        )

        cost_per_mw_inr = 50_000_000

        additional_installation_percentage = 10.0

        # --------------------------------------------------
        # 10.1 Annual Revenue
        # --------------------------------------------------

        revenue = (
            self.financial_service.estimate_annual_revenue(
                annual_energy_mwh=annual_energy_mwh,
                electricity_tariff_inr_per_kwh=
                    electricity_tariff
            )
        )

        # --------------------------------------------------
        # 10.2 Project Cost
        # --------------------------------------------------

        project_cost = (
            self.financial_service.estimate_project_cost(
                installed_capacity_mw=installed_capacity_mw,
                cost_per_mw_inr=cost_per_mw_inr,
                additional_installation_percentage=
                    additional_installation_percentage
            )
        )

        # --------------------------------------------------
        # 10.3 Payback Period
        # --------------------------------------------------

        payback = (
            self.financial_service.calculate_payback_period(
                total_project_cost_inr=(
                    project_cost[
                        "estimated_total_project_cost_inr"
                    ]
                ),
                annual_revenue_inr=(
                    revenue[
                        "estimated_annual_revenue_inr"
                    ]
                )
            )
        )

        # --------------------------------------------------
        # 10.4 ROI
        # --------------------------------------------------

        roi = (
            self.financial_service.calculate_roi(
                total_project_cost_inr=(
                    project_cost[
                        "estimated_total_project_cost_inr"
                    ]
                ),
                annual_revenue_inr=(
                    revenue[
                        "estimated_annual_revenue_inr"
                    ]
                )
            )
        )

        # --------------------------------------------------
        # 10.5 Combined Financial Result
        # --------------------------------------------------

        financial_analysis = {
            "annual_revenue": revenue,
            "project_cost": project_cost,
            "payback_period": payback,
            "roi": roi
        }



        
        return {
    "location": {
        "latitude": latitude,
        "longitude": longitude
    },

    "solar": { "class": solar_class }, "wind": wind_result,

    "site_suitability": evaluation,

    "recommended_deployment": deployment,

    "technical_feasibility": feasibility_result,

    "energy_yield": {
        "technology": energy_yield["technology"],
        "total_annual_energy_mwh": (
            energy_yield["total_annual_energy_mwh"]
        ),
        "total_annual_energy_gwh": (
            energy_yield["total_annual_energy_gwh"]
        )
    },

    "financial_metrics": {
        "annual_revenue": (
            financial_analysis["annual_revenue"][
                "estimated_annual_revenue_inr"
            ]
        ),

        "estimated_project_cost": (
            financial_analysis["project_cost"][
                "estimated_total_project_cost_inr"
            ]
        ),

        "payback_period": (
            financial_analysis["payback_period"][
                "payback_period_years"
            ]
        ),

        "roi": (
            financial_analysis["roi"][
                "roi_percentage"
            ]
        )
    },

    "recommendation_reason": (
        self._generate_recommendation_reason(
            evaluation=evaluation,
            deployment=deployment,
            feasibility=feasibility_result,
            financial_analysis=financial_analysis
        )
    )
}



        
    def _generate_recommendation_reason(
        self,
        evaluation,
        deployment,
        feasibility,
        financial_analysis
    ):
        reasons = []

        if evaluation.get("constraints_satisfied"):
            reasons.append(
                "The site satisfies the required site constraints."
            )
        else:
            reasons.append(
                "The site does not satisfy all required site constraints."
            )

        if feasibility.get("technically_feasible"):
            reasons.append(
                "The site is technically feasible for deployment."
            )
        else:
            reasons.append(
                "The site is not technically feasible for deployment."
            )

        reasons.append(
            f"Recommended deployment is {deployment}."
        )

        payback = financial_analysis.get(
            "payback_period",
            {}
        )

        if payback.get("payback_status") == "Recoverable":
            years = payback.get(
                "payback_period_years"
            )

            reasons.append(
                f"The estimated payback period is {years} years."
            )
        else:
            reasons.append(
                "The project is not financially recoverable "
                "under the current assumptions."
            )

        return " ".join(reasons)


