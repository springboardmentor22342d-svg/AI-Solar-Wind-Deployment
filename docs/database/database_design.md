# Database Design Draft

**Project:** Solar & Wind Deployment Intelligence Platform
**Database:** **Database:** PostgreSQL + PostGIS

---


## Implementation Status (Updated)

| Table (as designed) | Status | Notes |
|---|---|---|
| Users | ✅ Implemented | Matches original design |
| Projects | ✅ Implemented | Matches original design |
| Sites | ✅ Implemented (merged) | Combined with EnvironmentalData, SolarPrediction, and WindPrediction into a single table for simplicity — see note below |
| EnvironmentalData | ⚠️ Merged into Sites | Fields (forest_pct, settlement proximity, etc.) now live directly on the Sites table |
| SolarPrediction | ⚠️ Merged into Sites | Fields (GHI, GTI, OPTA) now live directly on the Sites table |
| WindPrediction | ⚠️ Merged into Sites | Fields (wind_speed_100m, power_density_100m) now live directly on the Sites table |
| SuitabilityScore | ⚠️ Computed live, not persisted | Scoring logic implemented (`GET /scoring/site`), but results aren't yet saved to a dedicated table |
| Reports | ⚠️ Implemented client-side only | Per-site PDF export via browser print (frontend); no backend table, no persisted report history |

**Design decision:** Environmental, solar, and wind data were merged directly into the Sites table instead of using separate linked tables, since each site currently has exactly one value per feature (not multiple historical readings). This avoids unnecessary joins for the current scope. If the project later needs to track multiple predictions per site over time (e.g., comparing model versions), these could be split back into separate tables at that point.

## 1. Users
Stores login credentials and role assignments for platform access.

| Column | Type | Notes |
|---|---|---|
| **user_id (PK)** | INT / UUID | Unique identifier |
| name | VARCHAR | Full name |
| email | VARCHAR | Unique, used for login |
| password_hash | VARCHAR | Never store plain text |
| role | ENUM | Renewable Energy Planner / GIS Analyst / Project Manager / Administrator |
| created_at | TIMESTAMP | Account creation date |

---

## 2. Projects
A project groups multiple candidate sites under one planning initiative (e.g., "Rajasthan Solar Expansion 2026").

| Column | Type | Notes |
|---|---|---|
| **project_id (PK)** | INT / UUID | Unique identifier |
| project_name | VARCHAR | Descriptive name |
| created_by (FK) | INT | References Users.user_id |
| region | VARCHAR | State/zone the project focuses on |
| created_at | TIMESTAMP | |
| status | ENUM | Draft / In Review / Approved |

---

## 3. Sites
Individual candidate locations being evaluated — this maps directly to each row of your `site_features.csv`.

| Column | Type | Notes |
|---|---|---|
| **site_id (PK)** | INT / UUID | Unique identifier |
| project_id (FK) | INT | References Projects.project_id |
| site_name | VARCHAR | e.g., nearest settlement name |
| latitude | FLOAT | |
| longitude | FLOAT | |
| state | VARCHAR | Derived via reverse geocoding |
| elevation | FLOAT | Meters |

---

## 4. EnvironmentalData
Raw environmental/infrastructure factors pulled for each site — the "input features" layer.

| Column | Type | Notes |
|---|---|---|
| **env_id (PK)** | INT / UUID | Unique identifier |
| site_id (FK) | INT | References Sites.site_id |
| forest_pct | FLOAT | From state land-use data |
| net_area_sown_pct | FLOAT | Agricultural land indicator |
| culturable_wasteland_pct | FLOAT | Preferred land type for deployment |
| nearby_settlement_count | INT | Infrastructure proxy |
| distance_to_nearest_settlement_km | FLOAT | Infrastructure proxy |

---

## 5. SolarPrediction
Model outputs specific to solar potential per site.

| Column | Type | Notes |
|---|---|---|
| **solar_pred_id (PK)** | INT / UUID | Unique identifier |
| site_id (FK) | INT | References Sites.site_id |
| ghi | FLOAT | Global Horizontal Irradiance |
| gti | FLOAT | Global Tilted Irradiance |
| optimum_tilt_angle | FLOAT | From OPTA raster |
| predicted_energy_output | FLOAT | Model-generated estimate |
| model_version | VARCHAR | Tracks which model produced this |

---

## 6. WindPrediction
Model outputs specific to wind potential per site.

| Column | Type | Notes |
|---|---|---|
| **wind_pred_id (PK)** | INT / UUID | Unique identifier |
| site_id (FK) | INT | References Sites.site_id |
| wind_speed_100m | FLOAT | |
| power_density_100m | FLOAT | |
| predicted_energy_output | FLOAT | Model-generated estimate |
| model_version | VARCHAR | |

---

## 7. SuitabilityScore
The combined weighted score — output of your Site Scoring Engine (per your project's weighted model: 35% resource availability, 25% geographic suitability, 15% infrastructure, 15% environmental impact, 10% economic feasibility).

| Column | Type | Notes |
|---|---|---|
| **score_id (PK)** | INT / UUID | Unique identifier |
| site_id (FK) | INT | References Sites.site_id |
| resource_score | FLOAT | Weighted solar/wind component |
| geographic_score | FLOAT | Terrain/elevation component |
| infrastructure_score | FLOAT | Settlement proximity component |
| environmental_score | FLOAT | Land-use component |
| overall_score | FLOAT | Final weighted total |
| suitability_category | ENUM | Excellent / Highly Suitable / Moderately Suitable / Low Suitability / Unsuitable |

---

## 8. Reports
Generated output documents for a project or site.

| Column | Type | Notes |
|---|---|---|
| **report_id (PK)** | INT / UUID | Unique identifier |
| project_id (FK) | INT | References Projects.project_id |
| generated_by (FK) | INT | References Users.user_id |
| report_type | ENUM | Site Assessment / Feasibility / Investment |
| file_format | ENUM | PDF / Excel |
| generated_at | TIMESTAMP | |

---

## Relationships Overview
Users ──< Projects ──< Sites ──< EnvironmentalData
│
├──< SolarPrediction
├──< WindPrediction
└──< SuitabilityScore
Projects ──< Reports

(One user creates many projects → one project has many sites → each site has one environmental record, one solar prediction, one wind prediction, and one suitability score → each project can generate many reports.)