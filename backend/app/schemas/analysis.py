from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List

class AnalysisRequest(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    site_name: Optional[str] = Field(None, max_length=200)

class DeploymentRecommendation(BaseModel):
    recommended_technology: str
    confidence: int
    reason: str
    solar_class: str
    wind_class: str

class CriteriaEvaluationItem(BaseModel):
    value: float
    status: str

class CriteriaEvaluation(BaseModel):
    solar_irradiance: CriteriaEvaluationItem
    wind_speed: CriteriaEvaluationItem
    slope: CriteriaEvaluationItem
    distance_to_grid: CriteriaEvaluationItem
    distance_to_road: CriteriaEvaluationItem

class EvaluationSummary(BaseModel):
    overall_score: float
    criteria_evaluation: CriteriaEvaluation
    constraints: Dict[str, bool]
    failed_constraints: List[str]

class TechnicalFeasibility(BaseModel):
    is_feasible: bool
    feasibility_score: float
    failed_hard_constraints: List[str]
    constraint_summary: str

class EnergyYield(BaseModel):
    solar_energy_mwh: float
    wind_energy_mwh: float
    total_energy_mwh: float

class FinancialMetrics(BaseModel):
    annual_revenue: float
    estimated_project_cost: float
    estimated_opex: float
    payback_period: float
    roi: float

class PillarScores(BaseModel):
    resource_availability: float
    geographic_suitability: float
    infrastructure_access: float
    environmental_impact: float
    economic_feasibility: float

class GeospatialAnalytics(BaseModel):
    terrain_slope: float
    ndvi: float
    zoning_status: str
    land_cover: str

class MonthlyYield(BaseModel):
    month: str
    solar_gwh: float
    wind_gwh: float

class AnalysisResponse(BaseModel):
    site_id: Optional[str] = None
    site_name: Optional[str]
    latitude: float
    longitude: float
    features: Dict[str, Any]
    feature_importance: Optional[Dict[str, float]] = None
    evaluation: EvaluationSummary
    pillars: Optional[PillarScores] = None
    geospatial: Optional[GeospatialAnalytics] = None
    technical_feasibility: Optional[TechnicalFeasibility] = None
    deployment: DeploymentRecommendation
    energy_yield: Optional[EnergyYield] = None
    financial_metrics: Optional[FinancialMetrics] = None
    forecast: Optional[List[Dict[str, Any]]] = None
    monthly_yields: Optional[List[MonthlyYield]] = None

    model_config = ConfigDict(from_attributes=True)
