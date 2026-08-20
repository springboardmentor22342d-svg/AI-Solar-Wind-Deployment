"""
app/services – Business logic layer.

The services layer sits between the API routes and the database/ML models.
It keeps route handlers thin and business logic testable.

Services implemented:
  - feature_builder.py      → Orchestrates all external data-source clients
  - solar_assessment.py     → Rule-based solar resource classification & CF estimation
  - wind_assessment.py      → Rule-based wind resource classification & CF estimation
  - deployment_strategy.py  → Hybrid deployment recommendation logic

Services planned:
  - solar_service.py   → Load NASA POWER data, run solar ML model
  - wind_service.py    → Load GWA data, run wind ML model
  - site_service.py    → Combine all datasets for suitability scoring
  - report_service.py  → Generate PDF/Excel reports from prediction data
  - auth_service.py    → User management, password validation
"""

from app.services.solar_assessment import (
    classify_solar_site,
    calculate_solar_class,
    calculate_solar_capacity_factor,
    get_solar_assessment_summary,
)
from app.services.wind_assessment import (
    classify_wind_site,
    calculate_wind_class,
    calculate_capacity_factor,
    get_wind_assessment_summary,
)
from app.services.deployment_strategy import (
    recommend_deployment,
    generate_reason,
    confidence_score,
)

__all__ = [
    # Solar Assessment
    "classify_solar_site",
    "calculate_solar_class",
    "calculate_solar_capacity_factor",
    "get_solar_assessment_summary",
    # Wind Assessment
    "classify_wind_site",
    "calculate_wind_class",
    "calculate_capacity_factor",
    "get_wind_assessment_summary",
    # Deployment Strategy
    "recommend_deployment",
    "generate_reason",
    "confidence_score",
]
