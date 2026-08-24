import joblib
import os
import pandas as pd
from app.feasibility.feasibility_engine import FeasibilityEngine
from app.services.energy_yield_service import EnergyYieldService
from app.services.financial_analysis_service import FinancialAnalysisService

MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "../../models/random_forest_model.pkl"
)

model = joblib.load(MODEL_PATH)


class ModelService:
    def __init__(self):
        self.energy_service = EnergyYieldService()
        self.financial_service = FinancialAnalysisService()

    def predict(self, wind_speed, temperature, humidity, date):

        date = pd.to_datetime(date)

        features = pd.DataFrame([{
            "wind_speed": wind_speed,
            "temperature": temperature,
            "humidity": humidity,
            "year": date.year,
            "month": date.month,
            "day": date.day,
            "day_of_year": date.dayofyear
        }])

        prediction = model.predict(features)

        engine = FeasibilityEngine()

        feature = {
            "solar": float(prediction[0]) - (humidity/50),
            "wind": wind_speed,
            "temperature": temperature,
            "humidity": humidity,

            "slope": 10,
            "restricted_land": False,

            "road": 5,
            "grid": 3,

            "wind_capacity_factor": wind_speed/20
            
        }
        feasibility = engine.evaluate(feature)

        wind_capacity = min(1.0,wind_speed/20)

        energy_service = EnergyYieldService()
        solar_capacity=5
        wind_capacity=3
        system_efficiency=0.90
        electricity_tariff = 8
        installed_capacity = 8
        cost_per_mw = 7000000
        installation_percentage = 10

        solar_energy = self.energy_service.calculate_solar_yield(
            feature["solar"],
            solar_capacity,
            system_efficiency
        )
        wind_energy = self.energy_service.calculate_wind_yield(
            wind_capacity,
            feature["wind_capacity_factor"],
            system_efficiency
        )
        hybrid_energy = self.energy_service.calculate_hybrid_yield(solar_energy,wind_energy)
        annual_revenue = self.financial_service.calaculate_annual_revenue( 
            hybrid_energy,
            electricity_tariff
        )
        project_cost = self.financial_service.calculate_project_cost(
            installed_capacity,
            cost_per_mw,
            installation_percentage
        )
        payback = self.financial_service.calculate_payback_period(
            project_cost,
            annual_revenue
        )
        roi = self.financial_service.calculate_roi(
            annual_revenue,
            project_cost
        )
        print("NEW MODEL_SERVICE IS RUNNING")

        return {
            "prediction": float(prediction[0]),
            "technical_feasibile": feasibility["technical_feasible"],
            "feasibility_score": feasibility["feasibility_score"],
            "constraint_summary": feasibility["constraint_summary"],
            "final_recommendation": (
                "Site is technically feasible and suitable for deployment."
                if feasibility["technical_feasible"]
                else "Site is not technically feasible because one or more mandatory constraints failed."
            ),
            "energy_yield": {
                "annual_solar_energy_kwh": round(solar_energy,2) ,
                "annual_wind_energy_kwh": round(wind_energy,2),
                "annual_hybrid_energy_kwh": round(hybrid_energy,2),
                        },
            "financial_analysis": {
                "annual_revenue": round(annual_revenue,2),
                "estimated_project_cost": round(project_cost,2),
                "payback_peroid": round(payback,2) if payback else None,
                "roi": round(roi,2)
            },
            "top_features": [
                "Wind Speed",
                "Temperature",
                "Humidity"
            ],
            "explanation": "Prediction mainly influenced by Wind Speed, Temperature and Humidity."
        }