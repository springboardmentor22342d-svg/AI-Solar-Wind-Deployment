from pydantic import BaseModel
class SiteRequest(BaseModel):
    latitude: float
    longitude: float
class AnalysisResponse(BaseModel):
    site: dict
    solar: dict
    wind: dict
    score: dict
    recommendation: dict