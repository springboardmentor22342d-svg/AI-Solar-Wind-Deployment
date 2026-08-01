"""
Loads the trained Random Forest model ONCE at startup and serves
predictions for new coordinates. Model file lives in the project's
top-level models/ folder (per original project architecture), not
inside backend/ — path calculated relative to project root.
"""

import joblib
from pathlib import Path
from app.ml.feature_schema import SOLAR_MODEL_FEATURE_SCHEMA, WIND_MODEL_FEATURE_SCHEMA, build_model_input

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class MLPredictionService:
    """
    Generic prediction service — works for any trained regression
    model + matching feature schema, avoiding duplicated
    load/validate/predict logic per energy type.
    """

    def __init__(self, model_filename: str, schema: list, key_name: str):
        self.model = joblib.load(PROJECT_ROOT / "models" / model_filename)
        self.schema = schema
        self.key_name = key_name  # e.g. "wind_speed" — the model's primary driver feature

    def predict(self, features: dict) -> dict:
        model_input = build_model_input(features, self.schema)

        if any(v is None for v in model_input):
            missing = [self.schema[i] for i, v in enumerate(model_input) if v is None]
            return {"prediction_kwh_year": None, "error": f"Missing required features: {missing}"}

        prediction = self.model.predict([model_input])[0]
        return {"prediction_kwh_year": round(float(prediction), 2), "error": None}