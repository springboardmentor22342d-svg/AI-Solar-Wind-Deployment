# Module Responsibility Mapping

| Module | Input | Output | Location |
|---|---|---|---|
| Authentication | User credentials | JWT token | `app/api/auth.py` |
| Solar Prediction | NASA POWER data | Solar class, capacity factor | `app/services/solar_assessment.py` |
| Wind Prediction | Wind speed | Wind class, capacity factor | `app/services/wind_assessment.py` |
| Deployment Strategy | Solar class + Wind class | Solar / Wind / Hybrid recommendation | `app/services/deployment_strategy.py` |
| Feature Engineering | Lat/Lon | Aggregated feature dict | `app/services/feature_builder.py` |
| Site Suitability | Feature dict | Weighted suitability score | `app/services/site_scoring.py` |
| Site Analysis | Lat/Lon (API call) | Full evaluation report | `app/services/spatial/analysis_coordinator.py` |
| Energy Estimation | Capacity MW + CF% | Annual MWh | `app/services/energy_estimation.py` |
| Evaluation | Feature dict | Constraints + score + recommendation | `app/evaluation/evaluator.py` |
| Database | ORM models | PostgreSQL tables | `app/models/` |
| Reports | Prediction data | PDF / Excel output | `app/api/reports.py` |
| Dashboard | Prediction results | Graphs & Maps | `frontend/src/pages/DashboardPage.jsx` |
| API Services | HTTP requests | JSON responses | `app/api/` |
