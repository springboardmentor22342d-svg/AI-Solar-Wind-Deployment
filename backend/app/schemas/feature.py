from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FeatureCreate(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    solar_irradiance: Optional[float] = None
    wind_speed: Optional[float] = None
    temperature: Optional[float] = None
    humidity: Optional[float] = None
    elevation: Optional[float] = None
    slope: Optional[float] = None

    solar_irradiance_gti: Optional[float] = None
    optimum_tilt_angle: Optional[float] = None
    power_density_100m: Optional[float] = None
    nearby_settlement_count: Optional[int] = None
    distance_to_nearest_settlement_km: Optional[float] = None
    nearest_settlement_name: Optional[str] = None
    distance_to_road_km: Optional[float] = None
    distance_to_grid_km: Optional[float] = None
    forest_pct: Optional[float] = None
    net_area_sown_pct: Optional[float] = None
    fallow_land_pct: Optional[float] = None
    culturable_wasteland_pct: Optional[float] = None

class FeatureResponse(FeatureCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True