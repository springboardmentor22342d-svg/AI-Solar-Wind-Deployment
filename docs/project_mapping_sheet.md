# Project Mapping Sheet

**Project:** Solar & Wind Deployment Intelligence Platform
**Last updated:** [22 August]

| Module | Dataset(s) Used | Output |
|---|---|---|
| Solar Prediction | NASA POWER (GHI, GTI, OPTA rasters) | Solar energy output, optimum tilt angle |
| Wind Prediction | Global Wind Atlas (wind speed, power density @ 100m) | Wind energy output, capacity factor |
| Elevation/Terrain | District Elevation (SRTM-derived) | Site elevation |
| Infrastructure Accessibility | OpenStreetMap (India cities & towns) | Nearby settlement count, distance to nearest settlement |
| Environmental Impact | State-wise Land Use Pattern | Forest %, agricultural %, wasteland % |
| Site Suitability | Solar + Wind + Elevation + Infrastructure + Land Use (combined) | Weighted suitability score & category |
| Dashboard | Suitability Score + all prediction outputs | Graphs, maps, site comparison views |
| Authentication | N/A (user-provided credentials) | Secure JWT-based access control |
| Database & API Layer | Users, Projects, Sites data | Persistent storage + REST API access to all site data |
| Deployment Strategy | Solar + Wind classifications | Solar / Wind / Hybrid / Not Recommended, with confidence score and reasoning |
| Site Scoring Engine | Solar + Wind + Terrain + Infrastructure (real road/grid) + Environmental | Category scores + Overall Site Suitability Score, site ranking |
| Energy Estimation | Site features + deployment type + installed capacity | Annual energy output (kWh), profitability flag |
| Optimization Engine | Site features + land area | Recommended technology, capacity (MW), expansion status, remarks |


## Workflow

```
Raw Datasets (Solar rasters, Wind rasters, SRTM, OSM, Land Use)
   +
Live APIs (NASA POWER — solar_irradiance, temperature, humidity)
   ↓
FeatureBuilder (data_sources/ + services/feature_engineering/)
   ↓
Feature Store (PostgreSQL, cached, 1,310 clean sites)
   ↓
Evaluation Module (constraints → weighted score → recommendation)
   +
Deployment Strategy (rule-based Solar/Wind/Hybrid/Not Recommended)
   ↓
Live API layer (GET /evaluate, GET /deployment/recommend,
                 GET /solar/features, GET /features/compute,
                 GET /scoring/site, GET /optimization/plan)
   ↓
ML-based prediction models (Random Forest — solar & wind, implemented,
                             exposed via GET /predict/solar, GET /predict/wind)
   ↓
[Next phase: role-based access control; reports/export implemented client-side]
```

## Notes on deviations from original plan
- Infrastructure accessibility uses settlement-proximity (OSM cities/towns) instead of full road/substation network data, due to regional coverage limitations in available road shapefiles.
- Environmental impact uses state-level land-use percentages instead of pixel-level Sentinel satellite classification, to keep processing scope manageable within the internship timeline.
- Sites, Environmental, Solar, and Wind data were consolidated into a single database table (rather than 4 separate tables as in the original Task 6 design) to reduce complexity at the current project scale.


