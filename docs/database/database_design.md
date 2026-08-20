# Database Design
## Solar & Wind Deployment Intelligence Platform

*Updated: 11 July 2026 — Synced with actual SQLAlchemy ORM models*

---

## Overview

The database uses **PostgreSQL with PostGIS** extension. All tables are defined as SQLAlchemy ORM models inheriting from `DeclarativeBase`. Tables are created via `Base.metadata.create_all()` on startup (development) and managed via Alembic migrations (production).

---

## Table 1: `users`

**File:** `backend/app/models/user.py`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-incrementing user ID |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | User email (login credential) |
| `password_hash` | VARCHAR(255) | NOT NULL | bcrypt-hashed password |
| `full_name` | VARCHAR(255) | NULL | Display name |
| `role` | VARCHAR(50) | NOT NULL, DEFAULT 'user' | `'admin'` \| `'analyst'` \| `'user'` |
| `is_active` | BOOLEAN | NOT NULL, DEFAULT TRUE | Soft-disable without deleting |
| `created_at` | TIMESTAMP WITH TZ | DEFAULT NOW() | Auto-set on insert |
| `updated_at` | TIMESTAMP WITH TZ | ON UPDATE | Auto-updated on row change |

**Relationships (1:N):** users → solar_predictions, wind_predictions, site_analyses, reports, projects

---

## Table 2: `projects`

**File:** `backend/app/models/project.py`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Auto-incrementing project ID |
| `user_id` | INTEGER | FK → users.id, CASCADE DELETE, INDEX | Owner user |
| `project_name` | VARCHAR(255) | NOT NULL, INDEX | Deployment project name |
| `description` | TEXT | NULL | Optional project description |
| `state` | VARCHAR(100) | NOT NULL | Indian state / geographic region |
| `latitude` | FLOAT | NOT NULL | Geographic latitude (-90 to 90) |
| `longitude` | FLOAT | NOT NULL | Geographic longitude (-180 to 180) |
| `created_at` | TIMESTAMP WITH TZ | DEFAULT NOW() | Auto-set on insert |

---

## Table 3: `solar_predictions`

**File:** `backend/app/models/solar_prediction.py`

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PK | Auto-incrementing ID |
| `user_id` | INTEGER FK → users.id | CASCADE DELETE |
| `city_name` | VARCHAR(100) | Nearest city name |
| `latitude` | FLOAT NOT NULL | Site latitude |
| `longitude` | FLOAT NOT NULL | Site longitude |
| `input_year` | INTEGER | Year of input data |
| `solar_irradiance_kwh` | FLOAT | Annual kWh/m² (NASA POWER) |
| `clearness_index` | FLOAT | Solar clearness ratio 0–1 |
| `temp_mean_c` | FLOAT | Mean annual temperature °C |
| `humidity_pct` | FLOAT | Relative humidity % |
| `days_above_35c` | INTEGER | Extreme heat days |
| `predicted_output_kwh` | FLOAT | ML model output (kWh/m²/day) |
| `annual_generation_kwh` | FLOAT | Total annual energy |
| `panel_efficiency_pct` | FLOAT | Default 20% |
| `system_capacity_kw` | FLOAT | System size kW |
| `capacity_factor` | FLOAT | 0–1 efficiency ratio |
| `confidence_score` | FLOAT | Model confidence 0–1 |
| `model_version` | VARCHAR(50) | ML model version |
| `status` | VARCHAR(50) | 'completed' \| 'failed' |
| `created_at` | TIMESTAMP WITH TZ | Auto-set |

---

## Table 4: `wind_predictions`

**File:** `backend/app/models/wind_prediction.py`

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PK | Auto-incrementing ID |
| `user_id` | INTEGER FK → users.id | CASCADE DELETE |
| `city_name` | VARCHAR(100) | Nearest city name |
| `latitude` | FLOAT NOT NULL, INDEX | Site latitude |
| `longitude` | FLOAT NOT NULL, INDEX | Site longitude |
| `wind_speed_10m_ms` | FLOAT | NASA POWER station level (10m) |
| `wind_speed_50m_ms` | FLOAT | Global Wind Atlas hub height (50m) |
| `wind_speed_100m_ms` | FLOAT | GWA 100m hub height |
| `wind_power_density` | FLOAT | W/m² at site |
| `wind_consistency` | FLOAT | mean/std ratio |
| `high_wind_days` | INTEGER | Days with high wind |
| `elevation_m` | FLOAT | Site elevation (SRTM) |
| `roughness_length` | FLOAT | Terrain roughness, default 0.03 |
| `turbine_capacity_kw` | FLOAT | Default 2 MW |
| `hub_height_m` | FLOAT | Default 100m |
| `predicted_output_kwh` | FLOAT | Annual kWh per turbine |
| `capacity_factor` | FLOAT | 0–1 (>0.35 is good) |
| `wind_class` | INTEGER | NREL 1–7 (7 = best) |
| `confidence_score` | FLOAT | Model confidence |
| `status` | VARCHAR(50) | 'completed' \| 'failed' |
| `created_at` | TIMESTAMP WITH TZ | Auto-set |

---

## Table 5: `site_analyses`

**File:** `backend/app/models/site_analysis.py`

Stores multi-factor site suitability scoring from all 5 datasets.

| Group | Columns | Source |
|-------|---------|--------|
| Location | site_name, city_name, latitude, longitude, country, continent | User input |
| NASA POWER | solar_irradiance_kwh, clearness_index, wind_speed_ms, temp_mean_c, precip_total_mm | NASA POWER dataset |
| Global Wind Atlas | wind_speed_50m_ms, wind_speed_100m_ms | GWA dataset |
| SRTM | elevation_m, slope_deg | SRTM elevation dataset |
| Sentinel-2 | ndvi, ndwi, land_cover_class | Copernicus Sentinel |
| OpenStreetMap | dist_grid_km, dist_road_km | OSM infrastructure |
| Sub-scores (0–100) | solar_score (30%), wind_score (25%), terrain_score (20%), land_use_score (15%), infrastructure_score (10%) | Computed |
| Final | suitability_score (0–100), recommendation, notes, model_version | Computed |

---

## Table 6: `reports`

**File:** `backend/app/models/report.py`

| Column | Type | Description |
|--------|------|-------------|
| `id` | SERIAL PK | Auto-incrementing ID |
| `user_id` | INTEGER FK → users.id | CASCADE DELETE |
| `title` | VARCHAR(255) NOT NULL | Report title |
| `report_type` | VARCHAR(50) NOT NULL | 'solar' \| 'wind' \| 'site_analysis' \| 'comprehensive' |
| `file_path` | VARCHAR(500) | Path to generated PDF/Excel |
| `status` | VARCHAR(50) | 'generating' \| 'ready' \| 'failed' |
| `created_at` | TIMESTAMP WITH TZ | Auto-set |

---

## Entity Relationship Summary

```
users (1) ──< solar_predictions (N)
users (1) ──< wind_predictions  (N)
users (1) ──< site_analyses     (N)
users (1) ──< reports           (N)
users (1) ──< projects          (N)
```

All foreign keys use `ON DELETE CASCADE` — deleting a user removes all their data.

---

## RBAC Roles

| Role | Permissions |
|------|-------------|
| `admin` | Full access: user management, all data, admin endpoints |
| `analyst` | Can run predictions, generate reports, manage own projects |
| `user` | Basic access: view own data, manage own projects |

---

*Last updated: 11 July 2026 | Synchronized with actual ORM models*
