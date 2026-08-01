"""
Loads the trained Random Forest model ONCE at startup and serves
predictions for new coordinates. Model file lives in the project's
top-level models/ folder (per original project architecture), not
inside backend/ — path calculated relative to project root.
"""

import joblib
from pathlib import Path
from app.ml.feature_schema import SOLAR_MODEL_FEATURE_SCHEMA, build_model_input

# backend/app/services/ml_prediction_service.py -> parents[2] = project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]
MODEL_PATH = PROJECT_ROOT / "models" / "solar_energy_model_final.pkl"


class SolarPredictionService:
    def __init__(self):
        self.model = joblib.load(MODEL_PATH)

    def predict(self, features: dict) -> dict:
        model_input = build_model_input(features)

        if any(v is None for v in model_input):
            missing = [SOLAR_MODEL_FEATURE_SCHEMA[i] for i, v in enumerate(model_input) if v is None]
            return {"prediction_kwh_year": None, "error": f"Missing required features: {missing}"}

        prediction = self.model.predict([model_input])[0]
        return {"prediction_kwh_year": round(float(prediction), 2), "error": None}