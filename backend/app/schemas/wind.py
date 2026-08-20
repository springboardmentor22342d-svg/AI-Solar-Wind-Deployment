"""
app/schemas/wind.py – Pydantic schemas for Wind Prediction validation.

"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class WindPredictionRequest(BaseModel):
    city_name: Optional[str] = None
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    input_year: Optional[int] = None
    turbine_capacity_kw: float = Field(2000.0, gt=0)
    hub_height_m: float = Field(100.0, gt=0)


class WindPredictionResponse(BaseModel):
    id: int
    user_id: int
    city_name: Optional[str]
    latitude: float
    longitude: float
    
    # Inputs
    wind_speed_10m_ms: Optional[float]
    wind_speed_50m_ms: Optional[float]
    wind_power_density: Optional[float]
    elevation_m: Optional[float]
    
    # Config
    turbine_capacity_kw: float
    hub_height_m: float
    
    # Outputs
    predicted_output_kwh: Optional[float]
    capacity_factor: Optional[float]
    wind_class: Optional[int]
    
    # Meta
    confidence_score: Optional[float]
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
