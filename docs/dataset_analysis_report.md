# 📊 Dataset Analysis Report
## Solar & Wind Deployment Intelligence Platform
**Infosys Virtual Internship | Analysis Date: 3 July 2026**

---

## Executive Summary

This report presents a comprehensive analysis of all five datasets used in the Solar & Wind Deployment Intelligence Platform. The primary real-world dataset — **NASA POWER** — contains **6,651 rows × 53 columns** covering **190 world capital cities** across **35 years (1990–2024)**. The remaining four datasets (Global Wind Atlas, Sentinel-2, OpenStreetMap, SRTM) are currently placeholder/sample files pending download from Kaggle and will need to be expanded.

---

## 1. NASA POWER Dataset
**File:** `datasets/nasa_power/nasa_power_climate_risk_indices_190_capitals_1990_2024.csv`
**Size:** ~3.5 MB | **Source:** NASA POWER API / Kaggle

### 1.1 Dataset Dimensions

| Property | Value |
|---|---|
| **Total Rows** | 6,651 |
| **Total Columns** | 53 |
| **Cities Covered** | 190 world capitals |
| **Year Range** | 1990 – 2024 (35 years) |
| **Records per City** | 35 (one per year) |
| **File Size** | ~3.5 MB |

### 1.2 Column Inventory

The dataset is organized into **9 thematic groups**:

#### 🏙️ Location & Metadata (6 columns)
| Column | Type | Description | Sample Value |
|---|---|---|---|
| `city` | string | Capital city name | Abu Dhabi, Abuja, Accra |
| `iso_alpha3` | string | Country ISO 3-letter code | ARE, NGA, GHA |
| `latitude` | float | Geographic latitude (°) | 24.47 |
| `longitude` | float | Geographic longitude (°) | 54.37 |
| `continent` | string | Continent region | E.Mediterranean, Africa, Europe |
| `who_region` | string | WHO region code | EMR, AFR, EUR |
| `wb_income_group` | string | World Bank income group | High, LowerMid, Upper |
| `year` | int | Year of record | 1990–2024 |
| `data_days` | float | Days of data in that year | 365 / 366 (leap years) |

#### 🌡️ Temperature Variables (8 columns)
| Column | Unit | Description | Range Observed |
|---|---|---|---|
| `temp_mean_c` | °C | Annual mean temperature | ~−5 to ~35 °C |
| `temp_max_c` | °C | Highest daily max recorded | Up to 44°C+ |
| `temp_min_c` | °C | Lowest daily min recorded | Down to −17°C |
| `temp_std_c` | °C | Std dev of daily temps | Variability measure |
| `temp_range_mean_c` | °C | Mean daily temp range | ~3.5 to ~11 °C |
| `temp_seasonal_amp` | °C | Seasonal temperature amplitude | Higher in continental cities |
| `temp_yoy_change` | °C | Year-over-year change | −1 to +1.5 °C |
| `temp_5yr_mean` | °C | Rolling 5-year mean | Trend indicator |
| `temp_anomaly` | °C | Deviation from 5yr baseline | Climate signal |

#### 🔥 Extreme Temperature Events (4 columns)
| Column | Unit | Description | Example |
|---|---|---|---|
| `days_above_35c` | days | Days exceeding 35°C | Abu Dhabi: 128–161 days/yr |
| `days_above_40c` | days | Days exceeding 40°C | Abu Dhabi: 3–39 days/yr |
| `days_below_0c` | days | Freezing days | Zagreb: 49–106 days/yr |
| `days_below_minus10c` | days | Deep freeze days | Zagreb: 0–12 days/yr |
| `heat_stress_index` | days | Combined heat-humidity stress | High in tropical regions |
| `cold_stress_index` | days | Cold stress indicator | High in northern Europe |

#### ☀️ Solar Energy Variables (7 columns) — *Primary for Solar Module*
| Column | Unit | Description | Observed Range |
|---|---|---|---|
| `solar_total_mj` | MJ/m² | Total annual solar irradiation | 1,800–2,250 MJ/m² |
| `solar_mean_mj` | MJ/m²/day | Mean daily solar irradiation | ~4.9–6.2 MJ/m²/day |
| `solar_clear_mean_mj` | MJ/m²/day | Mean clear-sky irradiation | ~5.9–6.5 MJ/m²/day |
| `solar_clearness_idx` | 0–1 | Ratio of actual/clear-sky | 0.49–0.86 |
| `solar_peak_days` | days | Days of peak solar output | 0–1+ days/year |
| `solar_annual_kwh_m2` | kWh/m²/yr | Annual solar energy yield | ~499–620 kWh/m²/yr |
| `ideal_climate_days` | days | Days with ideal climate conditions | 100–165 days/yr |

> **Key Insight:** `solar_annual_kwh_m2` is the **most critical column** for the Solar Prediction Module. Abu Dhabi shows consistently high values (~545–620 kWh/m²/yr), confirming its suitability for solar deployment. Accra (Ghana) shows ~490–517 kWh/m²/yr — strong for equatorial Africa. Zagreb (Europe) shows ~337–390 kWh/m²/yr — lower due to latitude and cloud cover.

#### 💨 Wind Energy Variables (5 columns) — *Primary for Wind Module*
| Column | Unit | Description | Observed Range |
|---|---|---|---|
| `wind_mean_ms` | m/s | Annual mean wind speed | 2.2–4.1 m/s |
| `wind_max_ms` | m/s | Maximum wind gust recorded | 4.4–12.5 m/s |
| `wind_std_ms` | m/s | Wind speed variability | Consistency indicator |
| `high_wind_days` | days | Days with high wind events | 0–7 days/yr |
| `wind_power_density` | W/m² | Wind power density | 28–41 W/m² |

> **Key Insight:** `wind_mean_ms` and `wind_power_density` are primary inputs for the Wind Prediction Module. For practical wind turbine deployment, a minimum of **6–7 m/s** mean wind speed is typically needed. The `wind_mean_ms` in this dataset (2.2–4.1 m/s for capitals) reflects **low-level station observations**, not hub-height data. The Global Wind Atlas dataset (at 50m/100m height) will provide more accurate turbine-level wind speeds.

#### 🌧️ Precipitation Variables (7 columns)
| Column | Unit | Description | Observed Range |
|---|---|---|---|
| `precip_total_mm` | mm | Annual total precipitation | 10–2,094 mm |
| `precip_mean_mm` | mm/day | Mean daily precipitation | 0.03–5.7 mm/day |
| `precip_max_day_mm` | mm | Maximum single-day rainfall | 1.0–137 mm |
| `precip_std_mm` | mm | Precipitation variability | - |
| `precip_yoy_change` | mm | Year-over-year precipitation change | High variability |
| `days_heavy_rain` | days | Heavy rainfall days | 0–22 days/yr |
| `days_moderate_rain` | days | Moderate rainfall days | 0–166 days/yr |
| `days_dry` | days | Dry days per year | 100–365 days |

> **Key Insight:** Precipitation data helps assess flood risk at deployment sites and cloud cover impact on solar output. Abu Dhabi (desert climate) shows extremely low precipitation (10–327 mm/yr), while Abuja (tropical) shows 530–2,050 mm/yr. High precipitation correlates with higher cloud cover and lower solar clearness index.

#### 💧 Humidity Variables (4 columns)
| Column | Unit | Description | Observed Range |
|---|---|---|---|
| `rh_mean_pct` | % | Annual mean relative humidity | 58–85% |
| `rh_max_pct` | % | Maximum relative humidity | 79–99% |
| `dewpoint_mean_c` | °C | Mean dewpoint temperature | 6–24 °C |
| `humidity_stress_days` | days | Days with humidity-induced heat stress | 0–338 days/yr |

#### 🌍 Socioeconomic Variables (4 columns)
| Column | Unit | Description |
|---|---|---|
| `gdp_per_capita_usd` | USD | GDP per capita (country level) |
| `population` | count | National population |
| `urban_pop_pct` | % | Urban population percentage |
| `energy_use_kg_oil_eq` | kg oil eq. | Energy use per capita |

#### 🌡️ Atmospheric (3 columns)
| Column | Unit | Description |
|---|---|---|
| `pressure_mean_kpa` | kPa | Mean atmospheric pressure |
| `pressure_std_kpa` | kPa | Pressure variability |
| `climate_volatility` | index | Composite climate volatility score |

---

### 1.3 Data Quality Assessment

| Check | Finding | Status |
|---|---|---|
| **Missing values** | `temp_yoy_change`, `temp_5yr_mean`, `temp_anomaly`, `solar_clearness_idx` missing for year 1990 and 1991 (first years — no prior data for rolling calculations) | ✅ Expected |
| **Missing values** | `energy_use_kg_oil_eq` missing for 2024 (most recent year — data lag) | ✅ Expected |
| **Leap year detection** | `data_days` = 366 for 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024 — correctly identified | ✅ Correct |
| **Duplicate rows** | None detected (city + year is unique key) | ✅ Clean |
| **Negative precip values** | None found | ✅ Clean |
| **Outliers** | `precip_yoy_change` shows extreme swings (e.g., Abu Dhabi 2024: +218 mm YoY; Abuja 1999: −1081 mm) — drought/flood events | ⚠️ Natural but needs normalization before ML |
| **Temperature outliers** | Abu Dhabi 2024: temp_max = 44.02°C — consistent with climate trends | ✅ Valid |

### 1.4 Solar Energy Analysis – Top Observations

**Highest Solar Yield Locations (from sample):**
| City | Country | Avg Solar kWh/m²/yr | Solar Clearness | Climate |
|---|---|---|---|---|
| **Abu Dhabi** | UAE | ~575 kWh/m²/yr | 0.76–0.86 | Hot desert (BWh) |
| **Accra** | Ghana | ~500–515 kWh/m²/yr | 0.49–0.55 | Tropical Savanna (Aw) |
| **Abuja** | Nigeria | ~520–560 kWh/m²/yr | 0.52–0.57 | Tropical Savanna (Aw) |
| **Zagreb** | Croatia | ~337–390 kWh/m²/yr | 0.43–0.50 | Humid Continental (Dfb) |

**Trend (Abu Dhabi solar yield — 1990 to 2024):**
```
1990: 579 kWh/m²/yr  →  Peak solar year
2000: 614 kWh/m²/yr  →  Higher output
2010: 608 kWh/m²/yr  →  Stable high
2017: 575 kWh/m²/yr  →  Slight dip
2024: 554 kWh/m²/yr  →  Recent decline (more dust/humidity?)
```
> The slight declining trend in Abu Dhabi's solar yield post-2015 may reflect increasing aerosol loading (dust, pollution) — relevant for solar panel soiling analysis.

### 1.5 Temperature Trends – Climate Change Signal

**Abu Dhabi Mean Temperature Trend:**
```
1990: 27.7°C → 1995: 27.5°C → 2000: 27.9°C → 2005: 28.1°C 
→ 2010: 28.7°C → 2015: 28.5°C → 2020: 28.4°C → 2024: 28.8°C
```
> **~+1.1°C warming over 35 years** — consistent with global warming projections. Higher temperatures reduce solar panel efficiency (PV efficiency drops ~0.4%/°C above 25°C).

**Extreme Heat Days (Abu Dhabi — days >35°C per year):**
```
1990: 128 days → 2010: 140 days → 2021: 158 days → 2024: 150 days
```
> Increasing trend in extreme heat days impacts both solar panel performance and energy demand.

### 1.6 Wind Analysis – Key Findings

**Wind Power Density (Abu Dhabi):**
```
1990–2024 range: 28.9 – 41.5 W/m²
Mean: ~36 W/m²
```
> At 36 W/m², Abu Dhabi's station-level wind is classified as **Wind Class 1** (poor for utility-scale wind). However, offshore/elevated locations in the UAE may have significantly higher wind resources — the Global Wind Atlas at 100m hub height is essential for accurate assessment.

**Note on Wind Data Limitation:** The `wind_mean_ms` column in NASA POWER represents near-surface (~10m) meteorological station data. Real wind turbines operate at **80–120m hub height**, where wind speeds are typically **30–50% higher**. This is why the Global Wind Atlas dataset (which provides 50m/100m data) is critical for accurate wind prediction.

---

## 2. Global Wind Atlas Dataset
**File:** `datasets/global_wind_atlas/gwa_data.csv`
**Status:** ⚠️ **Sample data only (3 rows) — Real data needed**

### 2.1 Current Data
```
latitude | longitude | wind_speed_10m | wind_speed_50m
34       | -118      | 5.2            | 6.5
35       | -119      | 4.8            | 6.1
36       | -120      | 6.1            | 7.8
```

### 2.2 Column Analysis
| Column | Unit | Description | Project Role |
|---|---|---|---|
| `latitude` | ° | Site latitude | Geographic filter |
| `longitude` | ° | Site longitude | Geographic filter |
| `wind_speed_10m` | m/s | Wind speed at 10m AGL | Low-level reference |
| `wind_speed_50m` | m/s | Wind speed at 50m AGL | Turbine hub-height proxy |

### 2.3 Speed Ratio Observed
- 10m → 50m amplification factor: **~1.25–1.28×**
- This is consistent with wind shear profiles over flat terrain (power law exponent ~0.14)

### 2.4 Data Gap Analysis
| Missing Data | Priority | Source |
|---|---|---|
| `wind_speed_100m` | 🔴 High | GWA provides 100m data — essential for modern turbines |
| `wind_direction` | 🟡 Medium | Needed for turbine layout optimization |
| `wind_power_density` | 🟡 Medium | Directly usable for energy estimation |
| `capacity_factor` | 🟡 Medium | Key economic metric |
| Geographic coverage | 🔴 High | Current 3-row sample is insufficient |

> **Action Required:** Download real GWA data from [Kaggle GWA search](https://www.kaggle.com/search?q=Global+Wind+Atlas). The real dataset should have **100m wind speed data** across a geographic grid.

---

## 3. Sentinel-2 Dataset
**File:** `datasets/sentinel/sentinel2_data.csv`
**Status:** ⚠️ **Sample data only (3 rows) — Real data needed**

### 3.1 Current Data
```
latitude | longitude | ndvi | ndwi
34       | -118      | 0.6  | 0.1
35       | -119      | 0.4  | 0.2
36       | -120      | 0.7  | 0.3
```

### 3.2 Column Analysis
| Column | Range | Description | Project Role |
|---|---|---|---|
| `latitude` | ° | Site latitude | Geographic reference |
| `longitude` | ° | Site longitude | Geographic reference |
| `ndvi` | −1 to +1 | Normalized Difference Vegetation Index | Land cover type detection |
| `ndwi` | −1 to +1 | Normalized Difference Water Index | Water body detection |

### 3.3 NDVI Interpretation for Site Suitability
| NDVI Range | Land Type | Suitable for Deployment? |
|---|---|---|
| < 0.1 | Bare soil / desert | ✅ Excellent |
| 0.1 – 0.3 | Sparse vegetation / scrub | ✅ Good |
| 0.3 – 0.5 | Moderate vegetation | 🟡 Review needed |
| 0.5 – 0.7 | Dense shrubland | ❌ Avoid (ecological concern) |
| > 0.7 | Dense forest | ❌ Prohibited (forest conservation) |

> **Sample Observations:** NDVI values of 0.4–0.7 in the sample (California region) suggest moderate to dense vegetation — these sites would need environmental review before solar/wind installation.

### 3.4 Data Gap Analysis
| Missing Data | Priority |
|---|---|
| `land_cover_class` | 🔴 High — categorical land use label needed |
| `cloud_cover_pct` | 🟡 Medium — cloud cover affects solar irradiance |
| `slope` | 🟡 Medium — redundant with SRTM but useful cross-check |
| Large geographic grid | 🔴 High — 3 rows is insufficient |

---

## 4. OpenStreetMap (OSM) Infrastructure Dataset
**File:** `datasets/openstreetmap/osm_infrastructure.csv`
**Status:** ⚠️ **Sample data only (3 rows) — Real data needed**

### 4.1 Current Data
```
id | type       | dist_grid | dist_road
1  | substation | 10.5      | 2.1
2  | power_line | 0.0       | 5.5
3  | substation | 15.2      | 1.0
```

### 4.2 Column Analysis
| Column | Unit | Description | Project Role |
|---|---|---|---|
| `id` | int | Unique infrastructure feature ID (PK) | Record identification |
| `type` | string | Infrastructure type | Filter by category |
| `dist_grid` | km | Distance to nearest grid connection | Connection cost proxy |
| `dist_road` | km | Distance to nearest road | Accessibility factor |

### 4.3 Infrastructure Cost Impact
Connection cost to grid is one of the largest capital expenditure items in renewable energy deployment:

| Distance to Grid | Cost Impact | Suitability Score Modifier |
|---|---|---|
| 0–5 km | Low (readily connectable) | +20 pts |
| 5–15 km | Moderate | +10 pts |
| 15–30 km | High | −10 pts |
| > 30 km | Very High (may be uneconomic) | −25 pts |

### 4.4 Data Gap Analysis
| Missing Column | Priority | Purpose |
|---|---|---|
| `voltage_level` | 🟡 Medium | High-voltage lines preferred for large-scale projects |
| `lat`, `lon` | 🔴 High | Spatial join with site locations requires coordinates |
| `substation_capacity_mva` | 🟡 Medium | Determines how much generation can connect |
| `road_type` | 🟡 Low | Paved roads needed for heavy equipment access |

---

## 5. SRTM Elevation Dataset
**File:** `datasets/srtm/srtm_elevation.csv`
**Status:** ⚠️ **Sample data only (3 rows) — Real data needed**

### 5.1 Current Data
```
latitude | longitude | elevation | slope
34       | -118      | 150       | 2.5
35       | -119      | 200       | 5.0
36       | -120      | 50        | 1.2
```

### 5.2 Column Analysis
| Column | Unit | Description | Project Role |
|---|---|---|---|
| `latitude` | ° | Site latitude | Spatial reference |
| `longitude` | ° | Site longitude | Spatial reference |
| `elevation` | m | Height above sea level | Wind resource & logistics |
| `slope` | ° | Terrain slope angle | Installability check |

### 5.3 Site Suitability Thresholds
| Parameter | Suitable Range | Marginal | Unsuitable |
|---|---|---|---|
| **Slope (Solar)** | < 3° | 3°–10° | > 10° |
| **Slope (Wind)** | < 15° | 15°–25° | > 25° |
| **Elevation (Solar)** | 0–2,000 m | 2,000–3,500 m | > 3,500 m |
| **Elevation (Wind)** | 0–3,000 m | — | Mountain peaks |

> **Sample Observations:** All three sample points have slopes < 5.0° — all would pass the solar suitability slope test. Elevation 50–200m is ideal.

---

## 6. Cross-Dataset Integration Map

```
                    ┌─────────────────┐
                    │   NASA POWER    │
                    │ (6,651 records) │
                    │ solar_annual_   │
                    │ kwh_m2          │
                    │ wind_mean_ms    │
                    │ temp_mean_c     │
                    └────────┬────────┘
                             │ Join on: lat/lon proximity
              ┌──────────────┼──────────────┐
              │              │              │
    ┌─────────▼──────┐ ┌─────▼──────┐ ┌────▼────────┐
    │ Global Wind    │ │  Sentinel  │ │    SRTM     │
    │ Atlas          │ │    -2      │ │  Elevation  │
    │ wind_speed_50m │ │  ndvi      │ │  elevation  │
    │ wind_speed_100m│ │  land_cover│ │  slope      │
    └────────┬───────┘ └─────┬──────┘ └────┬────────┘
             │               │             │
             └───────────────┼─────────────┘
                             │
                    ┌────────▼────────┐
                    │  Site Score     │
                    │  Calculation    │
                    │                 │
                    │  Solar Score =  │
                    │  f(solar_kwh,   │
                    │    slope, ndvi, │
                    │    dist_grid)   │
                    │                 │
                    │  Wind Score =   │
                    │  f(wind_50m,    │
                    │    elevation,   │
                    │    slope,       │
                    │    dist_grid)   │
                    └─────────────────┘
                             │
                    ┌────────▼────────┐
                    │ OSM Infrastructure│
                    │ dist_grid       │
                    │ dist_road       │
                    └─────────────────┘
```

---

## 7. Feature Engineering Recommendations

For the ML prediction pipeline, the following derived features should be created:

### Solar Prediction Features
| Feature | Formula | Purpose |
|---|---|---|
| `solar_capacity_factor` | `solar_annual_kwh_m2 / (8760 × peak_watt)` | System efficiency metric |
| `cloud_penalty` | `1 - solar_clearness_idx` | Cloud impact on output |
| `temp_efficiency_factor` | `1 - 0.004 × (temp_mean_c - 25)` | PV temperature derating |
| `drought_risk_score` | `drought_stress_days / 365` | Water scarcity risk |

### Wind Prediction Features
| Feature | Formula | Purpose |
|---|---|---|
| `wind_hub_height_est` | `wind_mean_ms × (hub_height/10)^0.14` | Power law extrapolation |
| `wind_consistency` | `wind_mean_ms / wind_std_ms` | Wind reliability index |
| `wind_energy_density` | `0.5 × 1.225 × wind_mean_ms³` | Raw power potential |

### Site Suitability Features
| Feature | Components | Weight |
|---|---|---|
| `solar_potential_score` | solar_kwh_m2, clearness, temp_efficiency | 30% |
| `wind_potential_score` | wind_speed_50m, consistency | 25% |
| `terrain_score` | slope, elevation | 20% |
| `land_use_score` | ndvi, land_cover | 15% |
| `infrastructure_score` | dist_grid, dist_road | 10% |

---

## 8. Dataset Readiness Summary

| Dataset | Rows | Columns | Status | Priority Action |
|---|---|---|---|---|
| **NASA POWER** | 6,651 | 53 | ✅ Real data | Ready for EDA & ML pipeline |
| **Global Wind Atlas** | 3 | 4 | ⚠️ Sample only | Download real GWA data from Kaggle |
| **Sentinel-2** | 3 | 4 | ⚠️ Sample only | Download from Kaggle / Copernicus Hub |
| **OpenStreetMap** | 3 | 4 | ⚠️ Sample only | Download from Overpass API or Kaggle |
| **SRTM** | 3 | 4 | ⚠️ Sample only | Download from USGS / Kaggle |

---

## 9. Kaggle Dataset Download Links

| Dataset | Kaggle Search URL | Expected Format |
|---|---|---|
| NASA POWER | [kaggle.com/search?q=NASA+POWER](https://www.kaggle.com/search?q=NASA+POWER) | CSV |
| Global Wind Atlas | [kaggle.com/search?q=Global+Wind+Atlas](https://www.kaggle.com/search?q=Global+Wind+Atlas) | CSV / GeoTIFF |
| Sentinel-2 | [kaggle.com/search?q=Sentinel-2](https://www.kaggle.com/search?q=Sentinel-2) | GeoTIFF / CSV |
| OpenStreetMap | [kaggle.com/search?q=OpenStreetMap](https://www.kaggle.com/search?q=OpenStreetMap) | CSV / GeoJSON |
| SRTM | [kaggle.com/search?q=SRTM](https://www.kaggle.com/search?q=SRTM) | GeoTIFF / CSV |

---

## 10. Key Findings & Takeaways

> [!NOTE]
> **NASA POWER is production-ready.** 6,651 rows × 53 columns of real-world climate data spanning 35 years across 190 capitals is sufficient to build the Solar Prediction and Wind Prediction ML models.

> [!IMPORTANT]
> **Four datasets are sample stubs.** Global Wind Atlas, Sentinel-2, OSM, and SRTM need real data downloads before the Site Suitability module can function properly.

> [!TIP]
> **Top ML features from NASA POWER:** `solar_annual_kwh_m2`, `solar_clearness_idx`, `wind_mean_ms`, `wind_power_density`, `temp_mean_c`, `days_above_35c`, `humidity_stress_days` are the highest-value features for the prediction models.

> [!WARNING]
> **Wind speed at 10m is not suitable for turbine siting.** The NASA POWER `wind_mean_ms` is a ground-level observation (~10m). Hub heights for modern wind turbines are 80–150m. Always use GWA data (50m/100m) for wind project feasibility.

> [!CAUTION]
> **Preprocessing required before ML training.** Year 1990–1991 has ~7–8 missing values in rolling/anomaly columns. The `precip_yoy_change` column has extreme outliers (e.g., −1,081 mm). Apply winsorization or IQR-based clipping before model training.

---

## 11. Recommended Next Steps

### Immediate (Week 2)
1. **Download real datasets** from Kaggle links above — prioritize GWA at 100m height
2. **Run EDA notebook** (`notebooks/dataset_analysis.py`) against real data
3. **Implement preprocessing pipeline** in `backend/app/services/solar_service.py`
4. **Handle missing values** in NASA POWER (years 1990–1991, column `energy_use_kg_oil_eq` for 2024)

### Short-term (Week 2–3)
5. **Feature engineering** — create derived columns listed in Section 7
6. **Spatial join** — merge GWA + SRTM + Sentinel by lat/lon using GeoPandas
7. **Train baseline ML model** — Linear Regression on `solar_annual_kwh_m2`
8. **Validate model** — test against known solar irradiance values

### Long-term (Week 3–4)
9. **Deploy prediction API** — FastAPI endpoints calling trained model
10. **Integrate OSM** — compute `dist_grid` for candidate sites using GeoPandas spatial operations
11. **Build site scoring function** — combine all dataset features into 0–100 suitability score

---

*Report generated: 3 July 2026 | Infosys Virtual Internship – Day 3*
*Project: Solar & Wind Deployment Intelligence Platform*
