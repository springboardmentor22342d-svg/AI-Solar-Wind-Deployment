from app.ml.model_inference import ModelInference
from app.ml.feature_importance import FeatureImportance
from app.feasibility.feasibility_engine import FeasibilityEngine
from app.energy.energy_yield_service import EnergyYieldService
from app.financial.financial_analysis_service import FinancialAnalysisService


class PredictionService:

    def __init__(self):

        self.inference = ModelInference()

        self.feature_importance = FeatureImportance()

        self.feasibility = FeasibilityEngine()

        self.energy_service = EnergyYieldService()

        self.financial_service = FinancialAnalysisService()

    def predict(self, features, site):

        # -------------------------
        # ML Prediction
        # -------------------------
        prediction = self.inference.predict(features)

        # -------------------------
        # Explainability
        # -------------------------
        ranking = self.feature_importance.get_feature_importance()

        top_features = ranking[:3]

        explanation = (
            f"The prediction is mainly influenced by "
            f"{top_features[0]['feature']}, "
            f"{top_features[1]['feature']}, "
            f"and {top_features[2]['feature']}."
        )

        # -------------------------
        # Feasibility
        # -------------------------
        feasibility = self.feasibility.evaluate(site)

        # -------------------------
        # Energy Yield
        # -------------------------
        energy = self.energy_service.estimate(

            solar_irradiance=prediction,

            wind_speed=features[6],

            installed_capacity=site["installed_capacity"],

            capacity_factor=site["capacity_factor"],

            system_efficiency=site["system_efficiency"],

            operational_losses=site["operational_losses"]

        )

        # -------------------------
        # Financial Analysis
        # -------------------------
        financial = self.financial_service.analyze(

            annual_energy_yield=energy["hybrid_energy"],

            electricity_tariff=site["electricity_tariff"],

            installed_capacity=site["installed_capacity"],

            cost_per_kw=site["cost_per_kw"],

            installation_percentage=site["installation_percentage"]

        )

        return {

            "prediction": prediction,

            "top_features": top_features,

            "explanation": explanation,

            "feasibility": feasibility,

            "energy_yield": energy,

            "financial": financial

        }