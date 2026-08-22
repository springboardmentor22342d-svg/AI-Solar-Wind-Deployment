from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from app.database.database import Base

class Feature(Base):
    __tablename__ = "features"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Core fields (as specified by Task 1)
    solar_irradiance = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    elevation = Column(Float, nullable=True)
    slope = Column(Float, nullable=True)

    # Extended fields (full FeatureBuilder output — kept so nothing is lost)
    solar_irradiance_gti = Column(Float, nullable=True)
    optimum_tilt_angle = Column(Float, nullable=True)
    power_density_100m = Column(Float, nullable=True)
    nearby_settlement_count = Column(Integer, nullable=True)
    distance_to_nearest_settlement_km = Column(Float, nullable=True)
    nearest_settlement_name = Column(String, nullable=True)
    distance_to_road_km = Column(Float, nullable=True)
    distance_to_grid_km = Column(Float, nullable=True)
    forest_pct = Column(Float, nullable=True)
    net_area_sown_pct = Column(Float, nullable=True)
    fallow_land_pct = Column(Float, nullable=True)
    culturable_wasteland_pct = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())