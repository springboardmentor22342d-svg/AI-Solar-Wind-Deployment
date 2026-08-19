# Solar & Wind Deployment Intelligence Platform ☀️💨

An end-to-end, AI-powered renewable energy platform that recommends optimal deployment strategies for solar, wind, and hybrid projects by analyzing environmental, geospatial, climatic, technical feasibility, and financial investment metrics.

---

## 📋 Table of Contents
1. [Project Overview](#-project-overview)
2. [Machine Learning Model & Prediction Details](#-machine-learning-model--prediction-details)
3. [Ocean & Open Water Constraint Detection](#-ocean--open-water-constraint-detection)
4. [Datasets Used](#-datasets-used)
5. [System Architecture & Working Workflow](#-system-architecture--working-workflow)
6. [Key Performance Metrics & Model Evaluation](#-key-performance-metrics--model-evaluation)
7. [Prerequisites & Environment Setup](#-prerequisites--environment-setup)
8. [How to Run the Application](#-how-to-run-the-application)
9. [Comprehensive Testing & Test Cases Guide](#-comprehensive-testing--test-cases-guide)
10. [DevOps & Docker Setup](#-devops--docker-setup)

---

## 🌟 Project Overview

The **Solar & Wind Deployment Intelligence Platform** assists planners, sustainability consultants, and project developers in evaluating geographic sites for renewable energy installations.

### Core Capabilities:
- **Location-Based Geospatial Intelligence**: Extracts solar irradiance, wind speed, elevation, terrain slope, grid proximity, and road access for any coordinate.
- **AI-Powered Resource Forecasting**: Predicts solar irradiance using a hyper-tuned Random Forest Regressor with feature importance explainability.
- **Technical Feasibility & Constraint Evaluation**: Evaluates hard constraints (slope > 15°, protected zones, ocean/open water body detection) and soft infrastructure constraints.
- **Deployment Strategy Engine**: Recommends optimal technology (**Solar**, **Wind**, **Hybrid**, or **Unfeasible**) with continuous dynamic confidence scoring (e.g. 88.4%, 92.1%, 76.8%, 0% for ocean).
- **Financial & Investment ROI Analytics**: Computes annual energy generation (kWh), CAPEX project costs, annual revenue, Return on Investment (ROI %), and payback period (years).

---

## 🤖 Machine Learning Model & Prediction Details

### 1. Selected Model Architecture
- **Model**: Tuned `RandomForestRegressor` (`n_estimators=300`, `max_depth=10`, `min_samples_leaf=2`, `random_state=42`)
- **Library**: `scikit-learn`
- **Saved Model File**: `models/solar_random_forest.joblib`
- **Model Loading**: Managed dynamically via `ModelManager` and `ModelInference` without requiring retraining.

### 2. Model Optimization & Rationale
Hyperparameters were tuned (`n_estimators=300`, `max_depth=10`, `min_samples_leaf=2`) to reduce MAE from 0.5395 down to **0.4918** and boost validation variance explained ($R^2$) to **69.02%**.

### 3. Model Inputs & Feature Schema
The model uses **7 numerical features** as input:

| Feature Index | Feature Name | Unit / Range | Description |
|:---:|:---:|:---:|:---|
| `0` | `month` | 1 – 12 | Month of the observation |
| `1` | `day` | 1 – 31 | Day of the month |
| `2` | `day_of_year` | 1 – 365 | Day index in the calendar year |
| `3` | `week_of_year` | 1 – 52 | Week number in the year |
| `4` | `temperature` | °C (-10 to 50) | Ambient surface temperature |
| `5` | `humidity` | % (0 to 100) | Relative atmospheric humidity |
| `6` | `wind_speed` | m/s (0 to 25) | Wind speed at 10m height |

- **Target Variable**: `solar_irradiance` (kWh/m²/day)

### 4. Feature Importance & Explainability

| Rank | Feature | Importance Weight | Impact Description |
|:---:|:---|:---:|:---|
| **1** | `humidity` | **52.67%** | Cloud cover & atmospheric moisture heavily impact solar radiation |
| **2** | `wind_speed` | **15.91%** | Atmospheric air movements and cloud dissipation |
| **3** | `day_of_year` | **11.53%** | Seasonal solar declination angle & daylight duration |
| **4** | `temperature` | **10.74%** | Thermal conditions correlated with clear-sky solar radiation |
| **5** | `day` | **4.16%** | Intra-month weather variations |
| **6** | `week_of_year` | **4.02%** | Weekly weather cycles |
| **7** | `month` | **0.98%** | Macro seasonal trend indicator |

---

## 🌊 Ocean & Open Water Constraint Detection

Land-based solar PV and wind turbine deployments are physically unfeasible in open ocean and deep sea waters.
The platform implements geographical ocean detection (`is_ocean_coordinate`) and elevation checks:

1. **Ocean Coordinate Detection**: Coordinates falling within major ocean boundaries (Arabian Sea, Bay of Bengal, Indian Ocean, Pacific Ocean, Atlantic Ocean, Mediterranean Sea) or with elevation <= 0m are flagged.
2. **Hard Constraint Trigger**: Triggers hard constraint failure: `"Site is located in an ocean or open water body; land-based solar/wind plant deployment is not technically feasible."`
3. **Unfeasible Strategy & Zero Energy Output**: Recommendation is set to `"Unfeasible"` with 0.0% confidence, 0 kWh annual energy, $0 project cost, $0 revenue, and N/A payback period.

---

## 📊 Datasets Used

1. **NASA POWER Dataset (`datasets/nasa_power/solar_history.csv`)**:
   - **Purpose**: Historical daily solar irradiance, wind speed, temperature, and relative humidity observations.
   - **Sample Size**: ~1,096 historical daily data records.
   - **Live API Integration**: `NasaPowerClient` fetches live point daily irradiance data (`ALLSKY_SFC_SW_DWN`, `T2M`, `RH2M`) from `https://power.larc.nasa.gov/api/temporal/daily/point`.

2. **Global Wind Atlas (GWA)**:
   - **Purpose**: Wind resource classification, average wind speed, and capacity factor estimation.

3. **NASA SRTM Elevation Dataset**:
   - **Purpose**: Terrain elevation (m) and slope degree calculation for feasibility constraint checking.

4. **OpenStreetMap (OSM)**:
   - **Purpose**: Proximity analysis to road networks and transmission grid lines.

---

## 📐 Key Performance Metrics & Model Evaluation

- **Mean Absolute Error (MAE)**: $\text{MAE} = \frac{1}{n} \sum |y_i - \hat{y}_i|$
- **Root Mean Squared Error (RMSE)**: $\text{RMSE} = \sqrt{\frac{1}{n} \sum (y_i - \hat{y}_i)^2}$
- **R-Squared ($R^2$)**: Variance explained by the model

### Tuned Model Performance:

| Metric | Value | Improvement |
|:---|:---:|:---|
| **MAE** | **0.4918** kWh/m²/day | Reduced error by 8.8% |
| **RMSE** | **0.6752** kWh/m²/day | Reduced RMSE |
| **R² Score** | **0.6902** (69.02%) | Variance explained boosted |
| **MAPE** | **11.33%** | Improved percentage error |

---

## 🚀 How to Run the Application

### Step 1: Launch the Backend (FastAPI)

1. Open terminal in `backend/`:
   ```bash
   cd backend
   ```
2. Activate Virtual Environment & install requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Start backend dev server:
   ```bash
   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
   *FastAPI server running at `http://localhost:8000` (Swagger docs: `http://localhost:8000/docs`).*

---

### Step 2: Launch the Frontend (React + Vite)

1. Open terminal in `frontend/`:
   ```bash
   cd frontend
   ```
2. Install frontend packages & start server:
   ```bash
   npm install
   npm run dev
   ```
   *Frontend application running at `http://localhost:5173`.*

---

## 🧪 Comprehensive Testing & Test Cases Guide

### Test Case 1: Automated Pytest Suite Execution
```bash
cd backend
python -m pytest
```
**Expected Output**: `7 passed in ~8.00s` (100% test pass rate).

---

### Test Case 2: Valid Land Site Analysis API Request
```bash
curl -X POST "http://localhost:8000/analysis/" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 20.2961, "longitude": 85.8245}'
```
**Expected Outcome**: Returns HTTP `200 OK` with `Recommendation: Hybrid`, `Confidence: 68.9%`, `Feasibility: Highly Feasible`, and complete financial metrics.

---

### Test Case 3: Ocean Site Unfeasible Analysis Request
Test selecting an ocean location (e.g. Arabian Sea `Lat: 15.0`, `Lon: 65.0`):

```bash
curl -X POST "http://localhost:8000/analysis/" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 15.0, "longitude": 65.0}'
```
**Expected Outcome**: Returns HTTP `200 OK` with:
- `deployment.recommendation`: `"Unfeasible"`
- `deployment.confidence_score`: `0.0%`
- `deployment.reason`: `"The selected location is situated in an ocean or open water body. Construction of land-based solar/wind power plants is not technically feasible."`
- `feasibility.technical_feasible`: `false`
- `energy_estimation.total_annual_energy_kwh`: `0`

---

### Test Case 4: Backend Validation Error Handling
Send out-of-bound coordinates (e.g., `Latitude: 150`):

```bash
curl -X POST "http://localhost:8000/analysis/" \
  -H "Content-Type: application/json" \
  -d '{"latitude": 150, "longitude": 85.8245}'
```
**Expected Outcome**: Returns HTTP `400 Bad Request`: `{"detail": "Latitude must be between -90 and 90."}`.

---

## 🐳 DevOps & Docker Setup

```bash
cd backend
docker build -t solar-wind-backend .
docker run -d -p 8000:8000 --name solar-wind-service solar-wind-backend
```
