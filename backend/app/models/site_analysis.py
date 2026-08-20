"""
app/models/site_analysis.py – SQLAlchemy ORM model for site suitability analysis.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class SiteAnalysis(Base):
    """
    ORM model mapped to the 'site_analyses' table.

    Integrates data from all five datasets to produce a 0–100 suitability score.
    Both raw input values and computed sub-scores are stored for full traceability.
    """

    __tablename__ = "site_analyses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    site_name = Column(String(200), nullable=True)      # user-given name
    city_name = Column(String(100), nullable=True)       # nearest city
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    country = Column(String(100), nullable=True)
    continent = Column(String(100), nullable=True)

    solar_irradiance_kwh = Column(Float, nullable=True)  # annual kWh/m²
    clearness_index = Column(Float, nullable=True)        # 0–1
    wind_speed_ms = Column(Float, nullable=True)          # m/s at 10m
    temp_mean_c = Column(Float, nullable=True)
    precip_total_mm = Column(Float, nullable=True)

    wind_speed_50m_ms = Column(Float, nullable=True)     # m/s at 50m AGL
    wind_speed_100m_ms = Column(Float, nullable=True)    # m/s at 100m AGL

    elevation_m = Column(Float, nullable=True)           # metres above sea level
    slope_deg = Column(Float, nullable=True)             # terrain slope angle

    ndvi = Column(Float, nullable=True)                  # vegetation index -1 to 1
    ndwi = Column(Float, nullable=True)                  # water index
    land_cover_class = Column(String(100), nullable=True) # e.g. "Barren / Desert"

    dist_grid_km = Column(Float, nullable=True)          # km to nearest grid
    dist_road_km = Column(Float, nullable=True)          # km to nearest road

    solar_score = Column(Float, nullable=True)           # weight: 30%
    wind_score = Column(Float, nullable=True)            # weight: 25%
    terrain_score = Column(Float, nullable=True)         # weight: 20%
    land_use_score = Column(Float, nullable=True)        # weight: 15%
    infrastructure_score = Column(Float, nullable=True)  # weight: 10%

    suitability_score = Column(Float, nullable=True)     # 0–100 weighted composite
    recommendation = Column(String(50), nullable=True)   # text label

    notes = Column(Text, nullable=True)                  # analyst comments

    model_version = Column(String(50), default="v1.0")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="site_analyses")

    @property
    def recommendation_label(self) -> str:
        """Derive recommendation text from composite score."""
        if self.suitability_score is None:
            return "Unknown"
        if self.suitability_score >= 75:
            return "Highly Suitable"
        elif self.suitability_score >= 55:
            return "Suitable"
        elif self.suitability_score >= 35:
            return "Marginal"
        else:
            return "Unsuitable"

    def __repr__(self) -> str:
        return (
            f"<SiteAnalysis id={self.id} site={self.site_name} "
            f"score={self.suitability_score} ({self.recommendation})>"
        )
