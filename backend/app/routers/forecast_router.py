from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.prediction_service import PredictionService


router = APIRouter(
    prefix="/forecast",
    tags=["Forecast"]
)

service = PredictionService()


class ForecastRequest(BaseModel):

    # -------------------------------------------------
    # Machine Learning Features
    # -------------------------------------------------
    month: int
    day: int
    day_of_year: int
    week_of_year: int
    temperature: float
    humidity: float
    wind_speed: float

    # -------------------------------------------------
    # Technical Feasibility Inputs
    # -------------------------------------------------
    protected_area: bool
    water_body: bool
    slope: float
    land_area: float
    environmental_rating: float
    economic_rating: float
    distance_to_grid: float
    distance_to_road: float

    # -------------------------------------------------
    # Energy Yield Inputs
    # -------------------------------------------------
    installed_capacity: float
    capacity_factor: float
    system_efficiency: float
    operational_losses: float

    # -------------------------------------------------
    # Financial Inputs
    # -------------------------------------------------
    electricity_tariff: float
    cost_per_kw: float
    installation_percentage: float

    def to_feature_list(self):

        return [

            self.month,

            self.day,

            self.day_of_year,

            self.week_of_year,

            self.temperature,

            self.humidity,

            self.wind_speed

        ]

    def to_site_dictionary(self):

        return {

            # ---------------------------------
            # Feasibility
            # ---------------------------------
            "protected_area": self.protected_area,
            "water_body": self.water_body,
            "slope": self.slope,
            "land_area": self.land_area,
            "environmental_rating": self.environmental_rating,
            "economic_rating": self.economic_rating,
            "distance_to_grid": self.distance_to_grid,
            "distance_to_road": self.distance_to_road,

            # ---------------------------------
            # Energy Yield
            # ---------------------------------
            "installed_capacity": self.installed_capacity,
            "capacity_factor": self.capacity_factor,
            "system_efficiency": self.system_efficiency,
            "operational_losses": self.operational_losses,

            # ---------------------------------
            # Financial
            # ---------------------------------
            "electricity_tariff": self.electricity_tariff,
            "cost_per_kw": self.cost_per_kw,
            "installation_percentage": self.installation_percentage

        }


@router.post("/")
def forecast(request: ForecastRequest):

    try:

        result = service.predict(

            request.to_feature_list(),

            request.to_site_dictionary()

        )

        return {

            "success": True,

            # ---------------------------------
            # ML Prediction
            # ---------------------------------
            "predicted_solar_irradiance": round(
                result["prediction"],
                4
            ),

            # ---------------------------------
            # Technical Feasibility
            # ---------------------------------
            "technical_feasible":
                result["feasibility"]["technical_feasible"],

            "feasibility_score":
                result["feasibility"]["feasibility_score"],

            "recommendation":
                result["feasibility"]["recommendation"],

            "constraint_summary":
                result["feasibility"]["constraint_summary"],

            # ---------------------------------
            # Energy Yield
            # ---------------------------------
            "energy_yield":
                result["energy_yield"],

            # ---------------------------------
            # Financial Analysis
            # ---------------------------------
            "financial_analysis":
                result["financial"],

            # ---------------------------------
            # Explainability
            # ---------------------------------
            "top_features":
                result["top_features"],

            "explanation":
                result["explanation"]

        }

    except ValueError as error:

        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(error)}"
        )