"""
app/models/__init__.py – SQLAlchemy ORM data models.

SQL Key concepts used here:
  - Primary Key (PK): Unique identifier for every row in a table.
  - Foreign Key (FK): Links one table to another.

Tables implemented:
  - User            – Registered platform users
  - SolarPrediction – Results from solar energy predictions
  - WindPrediction  – Results from wind energy predictions
  - SiteAnalysis    – Site suitability scores
  - Report          – Generated report metadata
  - Project         – Solar/wind deployment projects

"""

from app.models.user import User
from app.models.solar_prediction import SolarPrediction
from app.models.wind_prediction import WindPrediction
from app.models.site_analysis import SiteAnalysis
from app.models.report import Report
from app.models.project import Project

# Export all models so Base.metadata.create_all() can see them
__all__ = [
    "User",
    "SolarPrediction",
    "WindPrediction",
    "SiteAnalysis",
    "Report",
    "Project",
]
