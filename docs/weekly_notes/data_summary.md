# Dataset Summary

**Project:** Solar & Wind Deployment Intelligence Platform
**Prepared by:** Nandhini
**Purpose:** Profile of all raw datasets used in the site-suitability pipeline — row/column counts, data types, missing values, and unnecessary columns, per Task 3 requirements.

---

## 1. NASA POWER — Solar Irradiance (GHI)
| Property | Value |
|---|---|
| Format | GeoTIFF raster |
| Dimensions | 12,800 × 12,800 pixels |
| Bands | 1 |
| Data type | float32 |
| CRS | EPSG:4326 |
| Missing value marker | NaN |

**Notes:** Raster data — each pixel represents a solar irradiance value at a specific location across India, rather than tabular rows/columns. No columns to drop; this is the core solar potential input.

---

## 2. NASA POWER — Global Tilted Irradiance (GTI)
| Property | Value |
|---|---|
| Format | GeoTIFF raster |
| Dimensions | 12,800 × 12,800 pixels |
| Bands | 1 |
| Data type | float32 |
| CRS | EPSG:4326 |
| Missing value marker | NaN |

**Notes:** Same structure as GHI, but accounts for panel tilt — used for realistic energy output estimates.

---

## 3. NASA POWER — Optimum Tilt Angle (OPTA)
| Property | Value |
|---|---|
| Format | GeoTIFF raster |
| Dimensions | 960 × 960 pixels |
| Bands | 1 |
| Data type | int32 |
| CRS | EPSG:4326 |
| Missing value marker | -9999 |

**Notes:** Lower resolution than GHI/GTI since optimum tilt angle changes more gradually across geography. Uses -9999 as an explicit missing-data flag rather than NaN — important to filter this value out during analysis, not treat it as a real angle.

---

## 4. Global Wind Atlas — Wind Speed (100m)
| Property | Value |
|---|---|
| Format | GeoTIFF raster |
| Dimensions | 11,404 × 12,627 pixels |
| Bands | 1 |
| Data type | float32 |
| CRS | EPSG:4326 |
| Missing value marker | NaN |

**Notes:** NaN regions correspond to areas outside the India boundary used during download (notably some disputed/border regions, identified during pipeline testing).

---

## 5. Global Wind Atlas — Power Density (100m)
| Property | Value |
|---|---|
| Format | GeoTIFF raster |
| Dimensions | 11,404 × 12,627 pixels |
| Bands | 1 |
| Data type | float32 |
| CRS | EPSG:4326 |
| Missing value marker | NaN |

**Notes:** Same coverage/structure as wind speed; power density is the more decision-relevant metric since it accounts for the cube relationship between wind speed and energy.

---

## 6. District Elevation Dataset
| Property | Value |
|---|---|
| Format | CSV |
| Rows | 626 |
| Columns | 4 |

| Column | Data Type | Missing Values |
|---|---|---|
| District | string | 0 |
| Latitude | float64 | 0 |
| Longitude | float64 | 0 |
| elevation | int64 | 0 |

**Notes:** Fully clean dataset, no missing values. All 4 columns are used in the pipeline — no unnecessary columns.

---

## 7. OpenStreetMap — India Cities & Towns
| Property | Value |
|---|---|
| Format | GeoJSON |
| Rows (features) | 7,990 |
| Property columns | 65 |

**Notes:** Contains extensive multilingual name fields (`name:ar`, `name:bn`, `name:de`, `name:fr`, `name:hi`, `name:ja`, `name:ru`, `name:ta`, `name:te`, etc. — 40+ language variants) along with metadata like `wikidata`, `wikipedia`, `source`, `old_name`. Only `name`, `place`, and the coordinate geometry are actually used in this pipeline.

**Unnecessary columns for this project:** all `name:*` / `old_name:*` language-variant fields, `wikidata`, `wikipedia`, `source*` fields, `capital`/`capital_1`/`is_capital` (not currently used for site scoring), `rank`, `place:cca`. These could be dropped in a cleaned copy of the file to reduce size, though the original raw file is kept as-is for reference.

---

## 8. State-wise Land Use Pattern
| Property | Value |
|---|---|
| Format | CSV |
| Rows | 70 |
| Columns | 12 |

| Column | Data Type | Missing Values |
|---|---|---|
| States/UTs | string | 0 |
| Category | string | 0 |
| Total geographical area | float64 | 34 |
| Reporting area for land utilization | int64 | 0 |
| Forests | float64 | 2 |
| Not available for cultivation | float64 | 0 |
| Permanent pastures and other grazing lands | float64 | 4 |
| Land under miscellaneous tree crops & groves | float64 | 2 |
| Culturable wasteland | float64 | 2 |
| Fallow lands other than current fallows | float64 | 5 |
| Current fallows | float64 | 4 |
| Net area sown | float64 | 0 |

**Notes:** Contains a data-entry typo — `"Mahrashtra"` instead of `"Maharashtra"` — identified and corrected via a name-mapping dictionary in the pipeline code rather than editing the source file. `Total geographical area` has the most missing values (34/70), likely due to smaller Union Territories not reporting this figure separately.

**Unnecessary columns for this project:** `Not available for cultivation`, `Permanent pastures and other grazing lands`, and `Land under miscellaneous tree crops & groves` are not currently used in the site-scoring logic, though they could be incorporated into a more detailed environmental-impact factor in the future.

---

## Summary Table

| Dataset | Format | Rows/Pixels | Columns | Missing Data |
|---|---|---|---|---|
| Solar GHI | Raster | 12,800 × 12,800 | 1 band | NaN (outside coverage) |
| Solar GTI | Raster | 12,800 × 12,800 | 1 band | NaN (outside coverage) |
| Solar OPTA | Raster | 960 × 960 | 1 band | -9999 flag |
| Wind Speed 100m | Raster | 11,404 × 12,627 | 1 band | NaN (border regions) |
| Power Density 100m | Raster | 11,404 × 12,627 | 1 band | NaN (border regions) |
| District Elevation | CSV | 626 | 4 | None |
| OSM Towns/Cities | GeoJSON | 7,990 | 65 properties | Varies by field |
| State Land Use | CSV | 70 | 12 | Up to 34 (1 column) |



## Known Data Limitation: Border Region Coverage

54–55 candidate sites in Jammu & Kashmir/Ladakh and Arunachal Pradesh were 
excluded from the final training dataset due to incomplete coverage in the 
Global Wind Atlas raster and state-name mismatches in reverse-geocoding for 
these disputed border regions. This is a known limitation of the underlying 
public datasets, not a pipeline error — confirmed by inspecting the specific 
affected coordinates. Final clean dataset: ~1,323 sites.

## Update: NASA POWER Live API Integration

Solar irradiance is now sourced from two complementary places:
- **Live NASA POWER API** (`data_sources/nasa_power.py`) — provides
  solar_irradiance, temperature, and humidity, fetched on-demand per
  coordinate. Includes in-memory caching to avoid duplicate calls
  when both solar and climate features are requested together.
- **Global Solar Atlas rasters** (`data_sources/global_solar_atlas.py`,
  renamed from the original nasa_power.py) — provides GHI, GTI, and
  Optimum Tilt Angle, which are not available via a simple live API.

**Known limitation:** the live API introduces a genuine network
dependency. If NASA's servers are unreachable, `solar_irradiance`,
`temperature`, and `humidity` return null gracefully rather than
crashing the application (verified via deliberate URL-break test).
Raster-based fields remain available regardless of network status.

## Update: Raster/Vector Processor Skeletons Implemented

RasterProcessor and VectorProcessor (app/spatial/) were implemented
as generic, reusable wrappers — RasterProcessor for any single-band
.tif file, VectorProcessor for point-based GeoJSON layers. Verified
against known values (Bhopal GHI, nearest settlement) to confirm
consistency with existing dataset-specific clients. VectorProcessor
currently supports Point geometries only; Line/Polygon support
(roads, protected zones) would require Shapely geometry operations
and is not yet implemented.

## Update: Deployment Confidence Score Corrected

The original confidence_score() formula rewarded high-ranked
resources but not decision clarity — a clearly poor site scored
only 60% confidence, which misrepresented certainty. The formula
was revised to measure decision extremity (how far from "moderate"
the average resource rank is) and solar/wind agreement (how closely
the two resources' ranks align), producing high confidence for
clear-cut cases (both excellent or both poor) and lower confidence
for ambiguous, mismatched cases. Verified against 4 test scenarios.


## Update: Real Road and Grid Distance Data

Replaced the settlement-distance proxy for infrastructure scoring
with real data:
- **Roads** (`data_sources/grid_infrastructure.py` — RoadClient):
  major roads (motorway, trunk, primary) from a one-time Overpass
  API bulk export, simplified from ~322MB raw geometry down to
  28,043 sample points (every 5th coordinate along each road) for
  efficient in-memory distance lookups. See
  notebooks/08_download_infrastructure_data.py and
  notebooks/09_simplify_roads.py.
- **Grid/Substations** (GridClient): substation locations from the
  same Overpass export, used directly (4.3MB, no simplification needed).

Both are one-time downloads, loaded into memory at server startup —
no live API calls occur during actual feature computation or scoring.

This replaces the earlier settlement-distance proxy used in the
Evaluation Module and Site Scoring Engine's infrastructure/economic
sub-scores, which is now considered superseded (though evaluator.py's
constraint checks may still reference the proxy — see note below).


## Update: Site Scoring Engine + Cross-Module Consistency Fix

Built app/scoring/ (normalization.py, category_scores.py, site_scorer.py,
ranking.py) implementing the project's official weighted scoring model
(35% Resource / 25% Terrain / 15% Infrastructure / 15% Environmental /
10% Economic). Exposed via GET /scoring/site and GET /scoring/rank-sample.

During integration, two bugs were found and fixed:
1. calculate_resource_score() referenced a non-existent "wind_speed" key
   instead of "wind_speed_100m", silently zeroing out wind's contribution.
2. app/evaluation/ (built earlier) still used distance_to_nearest_settlement_km
   as an infrastructure proxy after real road/grid data was added — updated
   to use distance_to_grid_km and distance_to_road_km, matching app/scoring/.

Verified: GET /evaluate and GET /scoring/site now produce consistent
overall scores (70.71 vs 70.70) for the same coordinate, confirming both
modules are aligned on the same real, current data sources.


## Update: Energy Estimation & Optimization Modules

Built app/services/energy_estimation.py, energy_estimation_service.py,
and app/optimization/ (constraints, capacity_planning, expansion_analysis,
deployment_plan). Exposed via GET /energy/estimate and GET /optimization/plan.

Key assumptions, since no dataset provides these directly:
- Land area is a user-provided input per project (not derivable from
  any available dataset).
- Land-use ratios (2.0 ha/MW solar, 6.0 ha/MW wind) and grid capacity
  limits are configurable constants based on typical industry ranges,
  not site-specific measured values.
- Profitability is a simplified minimum-viable-energy threshold
  (500,000 kWh/year default), not a full financial model — no cost,
  tariff, or capex data is available to compute true ROI.

Bug found and fixed during validation: the initial capacity planning
logic allocated 100% of available land to recommended capacity,
making expansion analysis always show "Not Expandable" regardless of
actual site size (since no land was ever left unused). Fixed by
introducing a 60% default utilization ratio (recommend_capacity_mw),
plus a dual ratio+absolute-hectare threshold in expansion analysis
(analyze_expansion_feasibility) — a small site and a large site with
the same land-utilization ratio no longer receive identical expansion
labels; both the proportion AND the absolute spare land now matter.



## Update: Unified Analysis Pipeline

Built app/services/analysis_service.py (AnalysisService) — the single
orchestration point for the full workflow: feature retrieval ->
evaluation -> scoring -> deployment recommendation. Exposed via
POST /analysis.

Design note (addresses Task 5's refactor requirement): FeatureBuilder.build()
is called exactly ONCE per analysis request; solar/wind subsets used
by the evaluation, scoring, and deployment modules are extracted from
this single result rather than re-fetched — avoiding duplicate NASA
POWER API calls and raster reads that would otherwise occur if each
module independently retrieved its own data.

Verified across multiple real coordinates (Bhopal, Chennai) and
invalid input (out-of-range latitude), confirming consistent,
correctly-ordered execution and graceful validation failure handling.


## Update: Feature Store Refreshed with Real SRTM + Infrastructure Data

Dropped and recreated the features table with two new columns
(distance_to_road_km, distance_to_grid_km), then re-ran the full
populate pipeline (1,378 sites). Verified: only 22/1,378 sites show
slope=0 (down from the earlier near-universal 0 caused by the
district-CSV approximation) — consistent with genuinely flat terrain
in specific regions, not a systemic calculation issue. Re-exported
final_training_dataset.csv (1,310 clean sites) from the refreshed data.

**Known deferred item:** the original Sites table (265 sites, populated
in an earlier session) was NOT refreshed with the same SRTM/infrastructure
updates, since the Features table has fully superseded it as the active
data source for all current endpoints (/analysis, /evaluate, /scoring/site,
etc.). Sites remains available via GET/POST /sites for basic project
management purposes but reflects older, less accurate elevation/slope
and lacks real road/grid distance data. Can be refreshed later using
the same import pattern (notebooks/06_populate_feature_store.py) if
it becomes actively needed.


## Update: ML Baseline Model — Solar Energy Prediction

Trained and compared two regression models predicting annual solar
energy output (kWh/year) for a 5000kW reference installation:

| Model | Train R² | Val R² | Train MAE | Val MAE |
|---|---|---|---|---|
| Decision Tree | 1.0000 | 0.9999 | 0.00 | 2183.26 |
| Random Forest | 0.9996 | 0.9998 | 1276.63 | 1886.47 |

Decision Tree shows textbook overfitting (zero training error).
Random Forest selected for deployment due to more realistic,
consistent train/validation performance — better expected
generalization to genuinely new coordinates.

**Note on target generation:** the training target was computed using
a continuous capacity-factor formula (calculate_solar_capacity_factor_continuous),
not the bucketed classify_solar_site() used elsewhere in the codebase —
the bucketed version collapsed too many distinct irradiance values into
identical targets, which would have produced an artificially degenerate
regression problem.

Feature Schema (13 inputs, fixed order — see app/ml/feature_schema.py):
solar_irradiance, elevation, slope, forest_pct, net_area_sown_pct,
fallow_land_pct, culturable_wasteland_pct, distance_to_road_km,
distance_to_grid_km, distance_to_nearest_settlement_km,
nearby_settlement_count, temperature, humidity.

Model persisted via joblib to models/solar_energy_model_final.pkl
(project root, per original architecture). Loaded once at FastAPI
startup (app.state.solar_prediction_service), exposed via
GET /predict/solar.


## Update: Wind ML Model + Generalized Prediction Service

Trained and compared Random Forest vs. XGBoost for wind energy
prediction:

| Model | Train time (s) | Val MAE | Val RMSE | Val R² |
|---|---|---|---|---|
| Random Forest | 0.489 | 9,680.65 | 22,833.01 | 0.9999 |
| XGBoost | 0.128 | 36,780.13 | 70,192.14 | 0.9993 |

Random Forest selected despite XGBoost's faster training, due to a
much smaller train/validation performance gap (better generalization).
XGBoost's larger gap (train MAE 2,223 -> val MAE 36,780, ~16x) is
consistent with overfitting under default (untuned) hyperparameters —
a known XGBoost characteristic requiring more careful tuning than
Random Forest to avoid.

**Refactor:** SolarPredictionService was generalized into a single
reusable MLPredictionService class, parameterized by model file and
feature schema — avoiding duplicated load/validate/predict logic
between solar and wind prediction paths (see app/ml/feature_schema.py
for both schemas).

**Integration:** AnalysisService (POST /analysis) now uses ML
predictions for both solar and wind energy, replacing the earlier
rule-based energy_estimation.py calls for these two fields. The
response transparently reports prediction source ("ml_model" vs
"unavailable") and any missing-feature errors, verified via a live
edge-case test (Leh — a disputed border region with known land-use
data gaps) which correctly returned graceful null/error values
rather than crashing.