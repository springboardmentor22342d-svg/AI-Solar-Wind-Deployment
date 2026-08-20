"""
app/schemas/solar.py – Pydantic schemas for Solar Prediction validation.

"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class SolarPredictionRequest(BaseModel):
    city_name: Optional[str] = None
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    input_year: Optional[int] = None
    panel_efficiency_pct: float = Field(20.0, ge=1.0, le=100.0)
    system_capacity_kw: Optional[float] = Field(None, gt=0)


class SolarPredictionResponse(BaseModel):
    id: int
    user_id: int
    city_name: Optional[str]
    latitude: float
    longitude: float
    
    # Inputs
    solar_irradiance_kwh: Optional[float]
    clearness_index: Optional[float]
    temp_mean_c: Optional[float]
    
    # Outputs
    predicted_output_kwh: Optional[float]
    annual_generation_kwh: Optional[float]
    panel_efficiency_pct: float
    system_capacity_kw: Optional[float]
    capacity_factor: Optional[float]
    
    # Meta
    confidence_score: Optional[float]
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
