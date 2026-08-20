from pydantic import BaseModel, Field
from typing import Optional, Any, List, Union


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
    site_valid: bool
    validity_reasons: Optional[Union[List[str], str]] = None
    message: Optional[str] = None
    site_suitability: Optional[dict] = None
    recommended_deployment: Optional[dict] = None
    technical_feasibility: Optional[dict] = None
    energy_yield: Optional[dict] = None
    energy_yield_rating: Optional[dict] = None
    financial_metrics: Optional[dict] = None
    recommendation_reason: Optional[str] = None
    data_source: Optional[str] = None
    solar_rating: Optional[str] = None
    wind_rating: Optional[str] = None
    analysis_basis: Optional[str] = None
    raw_features: Optional[dict] = None
    nearby_installation: Optional[dict] = None