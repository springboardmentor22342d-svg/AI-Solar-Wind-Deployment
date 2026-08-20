"""
app/models/wind_prediction.py – SQLAlchemy ORM model for wind predictions.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class WindPrediction(Base):
    """
    ORM model mapped to the 'wind_predictions' table.

    Wind turbine energy output is primarily driven by wind speed at hub height
    (50m–150m AGL). The model stores both station-level (10m) and hub-height
    (50m from Global Wind Atlas) wind speeds for comparison.
    """

    __tablename__ = "wind_predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    city_name = Column(String(100), nullable=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    input_year = Column(Integer, nullable=True)

    wind_speed_10m_ms = Column(Float, nullable=True)    # m/s at 10m AGL (NASA POWER)
    wind_speed_50m_ms = Column(Float, nullable=True)    # m/s at 50m AGL (GWA)
    wind_speed_100m_ms = Column(Float, nullable=True)   # m/s at 100m AGL (GWA)
    wind_power_density = Column(Float, nullable=True)   # W/m²
    wind_consistency = Column(Float, nullable=True)     # mean/std ratio
    high_wind_days = Column(Integer, nullable=True)     # days with high wind

    elevation_m = Column(Float, nullable=True)          # from SRTM dataset
    roughness_length = Column(Float, default=0.03)      # terrain roughness

    turbine_capacity_kw = Column(Float, default=2000.0) # 2 MW standard turbine
    hub_height_m = Column(Float, default=100.0)         # 100m hub height

    predicted_output_kwh = Column(Float, nullable=True)  # annual kWh per turbine
    capacity_factor = Column(Float, nullable=True)        # 0–1 (>0.35 is good)
    wind_class = Column(Integer, nullable=True)           # NREL 1–7 (7=best)

    confidence_score = Column(Float, nullable=True)
    model_version = Column(String(50), default="v1.0")
    status = Column(String(50), default="completed")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="wind_predictions")

    def __repr__(self) -> str:
        return (
            f"<WindPrediction id={self.id} city={self.city_name} "
            f"wind_50m={self.wind_speed_50m_ms} m/s class={self.wind_class}>"
        )
