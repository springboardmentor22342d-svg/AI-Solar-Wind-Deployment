from pydantic import BaseModel, Field
from typing import Any, Dict


class AnalysisRequest(BaseModel):
    latitude: float = Field(
        ...,
        ge=-90,
        le=90
    )

    longitude: float = Field(
        ...,
        ge=-180,
        le=180
    )


class SolarResponse(BaseModel):
    class_: str = Field(
        ...,
        alias="class"
    )

    class Config:
        populate_by_name = True


class WindResponse(BaseModel):
    wind_class: str
    wind_speed: float | None = None

class SiteSuitabilityResponse(BaseModel):
    constraints_satisfied: bool
    overall_score: float
    recommendation: str
    failed_constraints: list


class TechnicalFeasibilityResponse(BaseModel):
    technically_feasible: bool
    hard_constraints: Dict[str, Any]
    soft_score: float
    decision: str


class EnergyYieldResponse(BaseModel):
    technology: str
    total_annual_energy_mwh: float
    total_annual_energy_gwh: float


class FinancialMetricsResponse(BaseModel):
    annual_revenue: float
    estimated_project_cost: float
    payback_period: float | None
    roi: float


class FinalAnalysisResponse(BaseModel):
    location: Dict[str, float]

    solar: SolarResponse

    wind: WindResponse

    site_suitability: SiteSuitabilityResponse

    recommended_deployment: str

    technical_feasibility: TechnicalFeasibilityResponse

    energy_yield: EnergyYieldResponse

    financial_metrics: FinancialMetricsResponse

    recommendation_reason: str