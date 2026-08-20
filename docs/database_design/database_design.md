# Database Design

## Users

| Column | Type | Description |
|---|---|---|
| id | SERIAL PK | Primary Key |
| email | VARCHAR(255) UNIQUE | User email |
| password_hash | VARCHAR(255) | Bcrypt hashed password |
| full_name | VARCHAR(255) | Display name |
| role | VARCHAR(50) | user / analyst / admin |
| is_active | BOOLEAN | Account status |
| created_at | TIMESTAMP | Registration time |

## Projects

| Column | Type | Description |
|---|---|---|
| id | SERIAL PK | Primary Key |
| user_id | INTEGER FK → users.id | Owner |
| project_name | VARCHAR(200) | Project title |
| description | TEXT | Details |
| state | VARCHAR(100) | Indian state |
| latitude | FLOAT | Decimal degrees |
| longitude | FLOAT | Decimal degrees |
| created_at | TIMESTAMP | Creation time |

## SolarPredictions

| Column | Type | Description |
|---|---|---|
| id | SERIAL PK | Primary Key |
| user_id | INTEGER FK | Owner |
| city_name | VARCHAR(100) | Location name |
| latitude / longitude | FLOAT | Coordinates |
| solar_irradiance_kwh | FLOAT | Annual kWh/m²/day |
| clearness_index | FLOAT | 0–1 |
| temp_mean_c | FLOAT | Mean temperature °C |
| predicted_output_kwh | FLOAT | Predicted annual output |
| capacity_factor | FLOAT | % |
| confidence_score | FLOAT | 0–100 |
| created_at | TIMESTAMP | Record time |

## WindPredictions

| Column | Type | Description |
|---|---|---|
| id | SERIAL PK | Primary Key |
| user_id | INTEGER FK | Owner |
| city_name | VARCHAR(100) | Location name |
| latitude / longitude | FLOAT | Coordinates |
| wind_speed_10m_ms | FLOAT | m/s at 10m |
| wind_speed_50m_ms | FLOAT | m/s at 50m |
| wind_speed_100m_ms | FLOAT | m/s at 100m |
| wind_power_density | FLOAT | W/m² |
| predicted_output_kwh | FLOAT | Annual output |
| capacity_factor | FLOAT | % |
| wind_class | INTEGER | 1–4 |
| confidence_score | FLOAT | 0–100 |
| created_at | TIMESTAMP | Record time |

## SiteAnalyses

| Column | Type | Description |
|---|---|---|
| id | SERIAL PK | Primary Key |
| user_id | INTEGER FK | Owner |
| site_name | VARCHAR(200) | Site label |
| latitude / longitude | FLOAT | Coordinates |
| solar_irradiance_kwh | FLOAT | Input feature |
| wind_speed_50m_ms | FLOAT | Input feature |
| elevation_m | FLOAT | Terrain |
| slope_deg | FLOAT | Terrain |
| ndvi / ndwi | FLOAT | Vegetation index |
| dist_grid_km | FLOAT | Infrastructure |
| dist_road_km | FLOAT | Infrastructure |
| solar_score | FLOAT | Sub-score |
| wind_score | FLOAT | Sub-score |
| terrain_score | FLOAT | Sub-score |
| land_use_score | FLOAT | Sub-score |
| infrastructure_score | FLOAT | Sub-score |
| suitability_score | FLOAT | Composite 0–100 |
| recommendation | VARCHAR(50) | e.g. Solar / Wind / Hybrid |
| created_at | TIMESTAMP | Analysis time |

## Reports

| Column | Type | Description |
|---|---|---|
| id | SERIAL PK | Primary Key |
| user_id | INTEGER FK | Owner |
| created_at | TIMESTAMP | Generation time |
