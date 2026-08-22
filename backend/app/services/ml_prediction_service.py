import joblib
from pathlib import Path
from app.ml.feature_schema import build_model_input

PROJECT_ROOT = Path(__file__).resolve().parents[3]


class MLPredictionService:
    def __init__(self, model_filename: str, schema: list, key_name: str,
                 top_features: list = None, primary_driver_label: str = None):
        self.model = joblib.load(PROJECT_ROOT / "models" / model_filename)
        self.schema = schema
        self.key_name = key_name
        self.top_features = top_features or [key_name]
        self.primary_driver_label = primary_driver_label or key_name

    def predict(self, features: dict) -> dict:
        model_input = build_model_input(features, self.schema)

        if any(v is None for v in model_input):
            missing = [self.schema[i] for i, v in enumerate(model_input) if v is None]
            return {"prediction_kwh_year": None, "error": f"Missing required features: {missing}", "explanation": None}

        prediction = self.model.predict([model_input])[0]

        from app.ml.feature_schema import build_explanation
        explanation = build_explanation(features, self.top_features, self.primary_driver_label)

        return {
            "prediction_kwh_year": round(float(prediction), 2),
            "error": None,
            "explanation": explanation,
            "top_contributing_features": self.top_features,
        }