from typing import List
from pydantic import BaseModel


class EnergyYieldResponse(BaseModel):
    annual_solar_energy_kwh: float
    annual_wind_energy_kwh: float
    annual_hybrid_energy_kwh: float


class FinancialAnalysisResponse(BaseModel):
    annual_revenue: float
    estimated_project_cost: float
    payback_peroid: float
    roi: float


class AnalysisResponse(BaseModel):
    prediction: float

    technical_feasibile: bool

    feasibility_score: float

    constraint_summary: List[str]

    final_recommendation: str

    energy_yield: EnergyYieldResponse

    financial_analysis: FinancialAnalysisResponse

    top_features: List[str]

    explanation: str