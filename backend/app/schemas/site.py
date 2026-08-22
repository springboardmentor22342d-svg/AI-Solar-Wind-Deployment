from pydantic import BaseModel, Field
from typing import Optional

class SiteCreate(BaseModel):
    name: str = Field(..., min_length=1)
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    ghi: Optional[float] = None
    gti: Optional[float] = None
    opta: Optional[float] = None
    wind_speed_100m: Optional[float] = None
    power_density_100m: Optional[float] = None
    elevation: Optional[float] = None
    nearby_settlement_count: Optional[int] = None
    distance_to_nearest_settlement_km: Optional[float] = None
    nearest_settlement_name: Optional[str] = None
    forest_pct: Optional[float] = None
    net_area_sown_pct: Optional[float] = None
    fallow_land_pct: Optional[float] = None
    culturable_wasteland_pct: Optional[float] = None

class SiteResponse(SiteCreate):
    id: int

    class Config:
        from_attributes = True