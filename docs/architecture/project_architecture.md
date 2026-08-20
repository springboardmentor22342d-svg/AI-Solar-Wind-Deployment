# Project Architecture – Solar & Wind Deployment Intelligence Platform

> **Infosys Virtual Internship | Day 3 – 2 July 2026**
> **Task:** Draw the Project Architecture Diagram

---

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              USER (Browser)                             │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │  HTTPS
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React.js)                             │
│                                                                         │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────┐  │
│   │  Auth Pages  │  │  Dashboard   │  │  Prediction  │  │ Reports  │  │
│   │  Login/Reg.  │  │  Maps/Charts │  │  Solar/Wind  │  │ PDF/XLSX │  │
│   └──────────────┘  └──────────────┘  └──────────────┘  └──────────┘  │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │  REST API (JSON)
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      API LAYER – FastAPI (Python)                       │
│                                                                         │
│   POST /api/v1/auth/login        → Authentication Module                │
│   POST /api/v1/auth/register     → User Registration                   │
│   POST /api/v1/solar/predict     → Solar Prediction Module             │
│   POST /api/v1/wind/predict      → Wind Prediction Module              │
│   POST /api/v1/site/analyze      → Site Suitability Module            │
│   GET  /api/v1/reports/generate  → Report Generation Module            │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
        ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐
        │   DATABASE    │  │  ML MODELS    │  │   DATASETS       │
        │  PostgreSQL   │  │               │  │                  │
        │  + PostGIS    │  │  ☀ Solar      │  │  📡 NASA POWER   │
        │               │  │    Model      │  │  💨 Wind Atlas   │
        │  Tables:      │  │  💨 Wind      │  │  🛰 Sentinel-2  │
        │  - users      │  │    Model      │  │  🗺 OpenStrMap  │
        │  - predictions│  │  📍 Site      │  │  🏔 SRTM        │
        │  - sites      │  │    Model      │  │                  │
        │  - reports    │  └───────────────┘  └──────────────────┘
        └───────────────┘
```

---

## Layered Architecture Diagram

```
╔═══════════════════════════════════════════════════════════╗
║                   PRESENTATION LAYER                      ║
║             React.js Frontend (Port 3000)                 ║
║   Dashboard │ Maps │ Prediction UI │ Auth │ Reports       ║
╠═══════════════════════════════════════════════════════════╣
║                    API GATEWAY LAYER                      ║
║            FastAPI Backend (Port 8000)                    ║
║     /auth   /solar   /wind   /site   /reports             ║
╠═══════════════════════════════════════════════════════════╣
║                   BUSINESS LOGIC LAYER                    ║
║                      Services/                            ║
║  AuthService │ SolarService │ WindService │ SiteService   ║
╠═══════════════════════════════════════════════════════════╣
║                     DATA ACCESS LAYER                     ║
║           SQLAlchemy ORM + ML Model Inference             ║
║    Models/ │ Schemas/ │ Database/ (sessions/queries)      ║
╠═══════════════════════════════════════════════════════════╣
║                    INFRASTRUCTURE LAYER                   ║
║    PostgreSQL + PostGIS    │    Datasets (CSV/GeoTIFF)    ║
║    (Docker: port 5432)     │    nasa_power / gwa / srtm   ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Data Flow Diagram

```
Datasets (CSV/GeoTIFF)
        │
        ▼
  Preprocessing
  (Pandas, GeoPandas, Rasterio)
        │
        ├──────────────────┬──────────────────┐
        ▼                  ▼                  ▼
  Solar Prediction   Wind Prediction    Site Suitability
  (NASA POWER)       (Global Wind       (NASA + Wind +
  → kWh/m²/day       Atlas)             SRTM + OSM)
                     → kWh/turbine      → Score 0–100
        │                  │                  │
        └──────────────────┴──────────────────┘
                           │
                     Dashboard &
                   Report Generation
                   (PDF / Excel / Maps)
```

---

## Module Interaction Map

```
┌─────────────────────────────────────────────────────────┐
│                    Project Modules                      │
│                                                         │
│  ┌─────────┐      ┌────────────────────────────────┐   │
│  │  Auth   │─────▶│  Protected Modules             │   │
│  │ Module  │      │  (requires valid JWT token)     │   │
│  └─────────┘      │                                │   │
│                   │  ┌──────────┐  ┌────────────┐  │   │
│                   │  │  Solar   │  │   Wind     │  │   │
│                   │  │Prediction│  │ Prediction │  │   │
│                   │  └────┬─────┘  └─────┬──────┘  │   │
│                   │       │              │          │   │
│                   │       └──────┬───────┘          │   │
│                   │              ▼                  │   │
│                   │  ┌─────────────────────┐        │   │
│                   │  │  Site Suitability   │        │   │
│                   │  │     Analysis        │        │   │
│                   │  └──────────┬──────────┘        │   │
│                   │             ▼                   │   │
│                   │  ┌─────────────────────┐        │   │
│                   │  │ Report Generation   │        │   │
│                   │  │   (PDF / Excel)     │        │   │
│                   │  └─────────────────────┘        │   │
│                   └────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## Database Schema (Simplified ER Diagram)

```
┌──────────────────┐          ┌──────────────────────┐
│      users       │          │   solar_predictions  │
│ ─────────────── │          │ ──────────────────── │
│ id (PK)          │◄────────│ user_id (FK)          │
│ email            │          │ id (PK)               │
│ password_hash    │          │ latitude              │
│ full_name        │          │ longitude             │
│ created_at       │          │ irradiance_kwh        │
│ is_active        │          │ predicted_output_kwh  │
└──────────────────┘          │ created_at            │
         ▲                    └──────────────────────┘
         │
         │                    ┌──────────────────────┐
         │                    │   wind_predictions   │
         │                    │ ──────────────────── │
         └────────────────────│ user_id (FK)          │
         │                    │ id (PK)               │
         │                    │ latitude              │
         │                    │ longitude             │
         │                    │ wind_speed_ms         │
         │                    │ predicted_output_kwh  │
         │                    │ created_at            │
         │                    └──────────────────────┘
         │
         │                    ┌──────────────────────┐
         │                    │   site_analyses      │
         │                    │ ──────────────────── │
         └────────────────────│ user_id (FK)          │
                              │ id (PK)               │
                              │ latitude              │
                              │ longitude             │
                              │ suitability_score     │
                              │ elevation_m           │
                              │ slope_deg             │
                              │ dist_grid_km          │
                              │ created_at            │
                              └──────────────────────┘
```

**SQL Key Concepts:**
- **PK (Primary Key):** Unique identifier for every row – e.g., `users.id`
- **FK (Foreign Key):** Links predictions back to the user who requested them – e.g., `solar_predictions.user_id → users.id`

---

## Technology Stack Summary

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | React.js | User interface, maps, charts |
| API | FastAPI (Python) | REST API, request routing |
| Auth | JWT + bcrypt | Secure authentication |
| ORM | SQLAlchemy 2.0 | Database abstraction |
| Database | PostgreSQL + PostGIS | Persistent data + geospatial |
| ML | scikit-learn | Solar/Wind/Site prediction |
| Data | Pandas, GeoPandas | Dataset processing |
| Containers | Docker + Docker Compose | Deployment |
| Migrations | Alembic | Database versioning |

---

*Created: 2 July 2026 | Infosys Virtual Internship – Day 3*
