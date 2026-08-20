"""
app/models/solar_prediction.py – SQLAlchemy ORM model for solar predictions.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database.database import Base


class SolarPrediction(Base):
    """
    ORM model mapped to the 'solar_predictions' table.

    Stores all inputs used for the solar prediction and the ML model output.
    Each record is linked to the requesting user via user_id (Foreign Key).
    """

    __tablename__ = "solar_predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    # ondelete="CASCADE": if the user is deleted, their predictions are too
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    city_name = Column(String(100), nullable=True)       # e.g. "Abu Dhabi"
    latitude = Column(Float, nullable=False)             # e.g. 24.47
    longitude = Column(Float, nullable=False)            # e.g. 54.37
    input_year = Column(Integer, nullable=True)          # e.g. 2024

    solar_irradiance_kwh = Column(Float, nullable=True)  # annual kWh/m²
    clearness_index = Column(Float, nullable=True)       # 0–1 solar clearness
    temp_mean_c = Column(Float, nullable=True)           # mean temperature °C
    humidity_pct = Column(Float, nullable=True)          # relative humidity %
    days_above_35c = Column(Integer, nullable=True)      # extreme heat days

    predicted_output_kwh = Column(Float, nullable=True)  # predicted daily kWh/m²
    annual_generation_kwh = Column(Float, nullable=True) # total annual generation
    panel_efficiency_pct = Column(Float, default=20.0)   # standard panel: 20%
    system_capacity_kw = Column(Float, nullable=True)    # system size kW
    capacity_factor = Column(Float, nullable=True)        # 0–1 efficiency ratio

    confidence_score = Column(Float, nullable=True)      # model confidence 0–1
    model_version = Column(String(50), default="v1.0")
    status = Column(String(50), default="completed")     # completed | failed

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="solar_predictions")

    def __repr__(self) -> str:
        return (
            f"<SolarPrediction id={self.id} city={self.city_name} "
            f"output={self.predicted_output_kwh} kWh/m²>"
        )
