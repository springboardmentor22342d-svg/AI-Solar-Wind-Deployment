from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Solar
    ghi = Column(Float)
    gti = Column(Float)
    opta = Column(Float)

    # Wind
    wind_speed_100m = Column(Float)
    power_density_100m = Column(Float)

    # Terrain
    elevation = Column(Float)

    # Infrastructure
    nearby_settlement_count = Column(Integer)
    distance_to_nearest_settlement_km = Column(Float)
    nearest_settlement_name = Column(String)

    # Land use
    forest_pct = Column(Float)
    net_area_sown_pct = Column(Float)
    fallow_land_pct = Column(Float)
    culturable_wasteland_pct = Column(Float)