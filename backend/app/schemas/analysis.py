from pydantic import BaseModel, Field
from typing import Optional, Any

class AnalysisRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    project_name: Optional[str] = None
    installed_capacity_kw: Optional[float] = 5000
    tariff_per_kwh: Optional[float] = 3.5


class AnalysisResponse(BaseModel):
    project_name: Optional[str]
    latitude: float
    longitude: float
    site_suitability: dict
    recommended_deployment: dict
    technical_feasibility: dict
    energy_yield: dict
    financial_metrics: dict
    recommendation_reason: str
    raw_features: dict