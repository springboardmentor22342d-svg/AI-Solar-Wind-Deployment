# API Reference

**Project:** Solar & Wind Deployment Intelligence Platform
**Base URL (local):** `http://127.0.0.1:8000`
**Interactive docs:** `http://127.0.0.1:8000/docs` (Swagger UI)

All endpoints return JSON. Endpoints marked 🔒 require a valid JWT token (see Authentication section for how to obtain one).

---

## General

### `GET /`
Welcome message, confirms the API is reachable.

**Response `200`:**
```json
{ "message": "Welcome to the Solar & Wind Deployment Intelligence Platform API" }
```

### `GET /health`
Confirms the application is running.

**Response `200`:**
```json
{ "status": "Running" }
```

### `GET /about`
Returns basic project identification.

**Response `200`:**
```json
{ "project": "Solar & Wind Deployment Intelligence Platform" }
```

---

## Authentication

### `POST /register`
Creates a new user account. Password is hashed before storage — never stored in plain text.

**Request body:**
```json
{
  "name": "Nandhini",
  "email": "nandhini@example.com",
  "password": "yourpassword",
  "role": "Renewable Energy Planner"
}
```

**Response `200`:**
```json
{
  "id": 1,
  "name": "Nandhini",
  "email": "nandhini@example.com",
  "role": "Renewable Energy Planner"
}
```

**Response `400`** — if the email is already registered.

---

### `POST /login`
Authenticates a user and returns a JWT access token.

**Request body:** (form data, not JSON — fields: `username`, `password`; `username` = the user's email)

**Response `200`:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Response `401`** — if email/password is incorrect.

**Using the token:** attach it as a header on protected requests:
Authorization: Bearer <access_token>

(In Swagger UI, click the "Authorize" button and paste the token there instead.)

---

## Projects

### `GET /projects`
Retrieves all stored projects. Public — no authentication required.

**Response `200`:**
```json
[
  {
    "id": 1,
    "project_name": "Test Solar Site",
    "description": "Verification run",
    "state": "Madhya Pradesh",
    "latitude": 23.26,
    "longitude": 77.41,
    "created_at": "2026-07-11T09:00:00Z"
  }
]
```

### `POST /projects` 🔒
Creates a new project. Requires a valid token.

**Request body:**
```json
{
  "project_name": "Rajasthan Wind Expansion",
  "description": "Phase 1 candidate sites",
  "state": "Rajasthan",
  "latitude": 26.9,
  "longitude": 70.9
}
```

**Validation rules:**
- `project_name`: required, cannot be empty
- `latitude`: required, must be between -90 and 90
- `longitude`: required, must be between -180 and 180
- `description`, `state`: optional

**Response `200`:** the created project, including auto-generated `id` and `created_at`.

**Response `422`** — if validation fails (e.g., empty name, out-of-range coordinates, missing required fields).

**Response `401`** — if no valid token is provided.

---

## Sites

### `GET /sites`
Retrieves all stored candidate sites, including full environmental/solar/wind feature data. Public — no authentication required.

**Response `200`:**
```json
[
  {
    "id": 1,
    "name": "Bhopal",
    "latitude": 23.2599,
    "longitude": 77.4126,
    "ghi": 5.196,
    "gti": 5.644,
    "opta": 26.0,
    "wind_speed_100m": 4.86,
    "power_density_100m": 113.04,
    "elevation": 495.0,
    "nearby_settlement_count": 9,
    "distance_to_nearest_settlement_km": 1.13,
    "nearest_settlement_name": "Ibrahimpura",
    "forest_pct": 28.28,
    "net_area_sown_pct": 47.91,
    "fallow_land_pct": 2.50,
    "culturable_wasteland_pct": 3.83
  }
]
```

Currently contains 265 real sites, imported from the project's processed dataset (`site_features.csv`), sourced from NASA POWER, Global Wind Atlas, SRTM-derived elevation data, OpenStreetMap, and state-wise land use records.

### `POST /sites` 🔒
Creates a new site record. Requires a valid token.

**Request body:** same shape as a `GET /sites` item, minus `id` (auto-generated). Only `name`, `latitude`, `longitude` are required; all environmental/solar/wind fields are optional.

**Response `200`:** the created site, including auto-generated `id`.

**Response `422`** — if validation fails (empty name, out-of-range coordinates).

**Response `401`** — if no valid token is provided.

---

## Planned (not yet implemented)

| Endpoint | Purpose | Target milestone |
|---|---|---|
| `POST /predictions/solar` | Predict solar output for a given site | Milestone 2 |
| `POST /predictions/wind` | Predict wind output for a given site | Milestone 2 |
| `GET /sites/{id}/suitability` | Return weighted suitability score for a site | Milestone 3 |
| `GET /reports/{project_id}` | Generate PDF/Excel report for a project | Milestone 4 |

---

## Authentication Notes

- Passwords are hashed using bcrypt via passlib — never stored or logged in plain text.
- Tokens are JWTs, valid for 60 minutes, signed with a secret key (currently hardcoded for development — flagged for migration to an environment variable before any deployment).
- Roles supported: Renewable Energy Planner, GIS Analyst, Project Manager, Administrator. Role-based permission enforcement (beyond basic login-required checks) is not yet implemented.

### `GET /solar/features`
Returns solar-specific features only (live + raster-based).
Query params: latitude, longitude.
Response `200`: {"solar_irradiance": float|null, "solar_irradiance_ghi": float, "solar_irradiance_gti": float, "optimum_tilt_angle": float}
Response `502`: if all values are null (total data retrieval failure).
Note: solar_irradiance may be null on network failure while raster
fields remain populated (partial degradation, not a full failure).

### `GET /deployment/recommend`
Returns a hybrid Solar/Wind/Hybrid deployment recommendation for a
coordinate, based on rule-based classification of solar and wind resources.
Query params: latitude, longitude.
Response `200`: {"deployment": str, "confidence": int, "reason": str, plus supporting classification fields}


### `POST /analysis`
Runs the complete site analysis pipeline in one call: retrieves solar
and wind features, evaluates constraints, calculates the composite
site score, and generates a deployment recommendation.

Request body: {"latitude": float, "longitude": float, "project_name": string (optional)}
Response `200`: consolidated result with solar_features, wind_features,
evaluation, site_score, deployment_recommendation, and raw_features.
Response `422`: invalid latitude/longitude.
Response `500`: pipeline execution failure (with error detail).


### `GET /predict/solar`
ML-based prediction of annual solar energy output (kWh/year) for a
5000kW reference installation, using a trained Random Forest model.
Query params: latitude, longitude.
Response `200`: {"latitude": float, "longitude": float, "prediction_kwh_year": float, "error": null}
Response includes "error" field (non-null) if required features are missing.