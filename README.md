# Solar & Wind Deployment Intelligence Platform

An AI-powered platform that evaluates coordinates across India for solar/wind renewable energy deployment suitability, combining real environmental data, trained ML models, technical feasibility engineering, and financial analysis.

## Current Implementation Status

### ✅ Fully Implemented & Tested
- Full data pipeline: solar (NASA POWER + Global Solar Atlas), wind (Global Wind Atlas), elevation (SRTM), infrastructure (OpenStreetMap), land use (state records), climate (NASA POWER)
- PostgreSQL backend with Feature Store caching
- JWT authentication
- Trained ML models: Random Forest for solar and wind energy prediction, compared against Decision Tree / XGBoost baselines
- Site Evaluation Engine (hard/soft constraints)
- Site Suitability Scoring Engine (weighted composite score)
- Deployment Recommendation (Solar/Wind/Hybrid decision logic)
- Technical Feasibility Engine
- Energy Yield Estimation (ML + rule-based fallback)
- Financial Analysis (revenue, cost, ROI, payback period)
- Land/water exclusion (Natural Earth land mask)
- Known-installation proximity flagging
- Unified `/analysis` API endpoint (single-call full pipeline)
- Frontend: single analysis screen with interactive map, authentication, and results dashboard
- Automated pytest test suite
- Docker containerization
- Database migrations (Alembic)

### 🔜 Planned / Not Yet Implemented
- Role-specific dashboards (GIS Analyst, Project Manager, Administrator views) — currently one unified analysis screen serves all users
- Notification & alert system
- PDF/Excel report export
- Forecasting model deployment (time-series input pipeline exists and is tested; forecasting *model* is a baseline seasonal-average implementation, not yet exposed via API)

See `docs/module_mapping.md` for detailed status per module.