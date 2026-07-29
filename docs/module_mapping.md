# Module Responsibility Mapping

**Project:** Solar & Wind Deployment Intelligence Platform
**Maps to backend structure:** `backend/app/{api, auth, database, models, schemas, services, utils}`

---

## 1. Authentication
| Aspect | Detail |
|---|---|
| Responsibility | User registration, login, JWT/OAuth2 token issuance, role-based access control |
| Inputs | Email, password, role |
| Outputs | Auth token, session validity |
| Backend location | `backend/app/auth/` |
| Related DB table | Users |

Status : Implemented - register, login, JWT tokens, protected routes

---

## 2. Solar Prediction
| Aspect | Detail |
|---|---|
| Responsibility | Extract GHI/GTI/OPTA values per site, run/apply solar output prediction model |
| Inputs | Site coordinates |
| Outputs | Predicted solar energy output, capacity factor |
| Backend location | `backend/app/services/solar_service.py` |
| Related DB table | SolarPrediction |

**Status:** ✅ Live feature retrieval implemented. Combines live NASA
POWER API (solar_irradiance, temperature, humidity) with Global Solar
Atlas rasters (GHI, GTI, optimum tilt angle). Exposed via
GET /solar/features. Prediction model (ML) not yet built — this is
feature engineering only.
---

## 3. Wind Prediction
| Aspect | Detail |
|---|---|
| Responsibility | Extract wind speed/power density per site, run wind output prediction model |
| Inputs | Site coordinates |
| Outputs | Predicted wind energy output, capacity factor |
| Backend location | `backend/app/services/wind_service.py` |
| Related DB table | WindPrediction |

**Status:** ✅ Feature retrieval implemented (Global Wind Atlas
rasters). Wind classification and capacity factor estimation
implemented via rule-based thresholds (wind_assessment.py) —
not yet ML-based. Exposed via GET /features/compute.
---

## 4. Site Suitability
| Aspect | Detail |
|---|---|
| Responsibility | Combine solar, wind, environmental, and infrastructure factors into the weighted suitability score |
| Inputs | Outputs of Solar Prediction, Wind Prediction, EnvironmentalData |
| Outputs | Overall suitability score + category (Excellent/Highly Suitable/etc.) |
| Backend location | `backend/app/services/suitability_service.py` |
| Related DB table | SuitabilityScore |

**Status:** ✅ Evaluation Module implemented (constraints, weighted
scoring, recommendation categories) — exposed via GET /evaluate.
Additionally, a separate Hybrid Deployment Strategy module
(deployment_strategy.py) determines Solar/Wind/Hybrid/Not Recommended
based on comparative resource classification — exposed via
GET /deployment/recommend. Both are rule-based; ML-based versions
are the next phase.

---

## 5. Database
| Aspect | Detail |
|---|---|
| Responsibility | Store/retrieve all persistent data (users, sites, predictions, scores, reports); manage relationships between tables |
| Inputs | Data from all other modules |
| Outputs | Query results for API/dashboard layer |
| Backend location | `backend/app/database/` |
| Related DB tables | All 8 tables |

Status : Implemented - postgresql

---

## 6. Reports
| Aspect | Detail |
|---|---|
| Responsibility | Generate PDF/Excel exports summarizing site assessments, feasibility, and investment recommendations |
| Inputs | SuitabilityScore, SolarPrediction, WindPrediction, Project data |
| Outputs | Downloadable report file |
| Backend location | `backend/app/services/report_service.py` |
| Related DB table | Reports |

Status : not started

---

## 7. Dashboard
| Aspect | Detail |
|---|---|
| Responsibility | Present role-specific visualizations (maps, scores, forecasts) to end users |
| Inputs | API responses (predictions, scores, reports) |
| Outputs | Rendered charts/maps/tables in the frontend |
| Frontend location | `frontend/` (React.js components) |
| Related modules | Consumes data from all backend services via API Services |

Status : not started

---

## 8. API Services
| Aspect | Detail |
|---|---|
| Responsibility | Expose backend functionality (auth, predictions, scoring, reports) to the frontend via REST endpoints |
| Inputs | HTTP requests from frontend/API clients |
| Outputs | JSON responses |
| Backend location | `backend/app/api/` |
| Framework | FastAPI |
| Related modules | Routes requests to Authentication, Solar/Wind Prediction, Site Suitability, Reports |

Status : Implemented - auth, projects, sites routers live, swagger-documented


## Energy Estimation
**Status:** ✅ Implemented. Calculates annual energy output (Solar/Wind/
Hybrid) using Installed Capacity × Capacity Factor × 8760 hours.
Includes a simplified profitability threshold check.

## Optimization / Deployment Planning
**Status:** ✅ Implemented. Recommends technology, capacity (MW),
and expansion feasibility based on land area and site resource
characteristics. Constraints (land use ratios, grid capacity) are
configurable, not data-derived.

## Analysis Pipeline (Integration Layer)
**Status:** ✅ Implemented. Orchestrates Solar, Wind, Evaluation,
Scoring, and Deployment modules into a single consolidated response
via POST /analysis. Single-responsibility design: AnalysisService
coordinates, but doesn't duplicate logic already implemented in
each underlying module.