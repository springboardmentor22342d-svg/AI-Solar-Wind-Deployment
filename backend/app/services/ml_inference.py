import os
import joblib
import numpy as np
import logging

logger = logging.getLogger(__name__)

class MLInferenceEngine:
    """
    Singleton class to load the ML model exactly once at startup
    and perform predictions.
    """
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLInferenceEngine, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        try:
            model_path = os.path.join(
                os.path.dirname(__file__), 
                '..', '..', 'models', 'best_baseline_model.joblib'
            )
            self._model = joblib.load(os.path.abspath(model_path))
            logger.info("Successfully loaded Random Forest baseline model.")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            self._model = None

    def predict_suitability(self, features: dict) -> tuple[float, dict]:
        """
        Takes raw features, validates them, and predicts the overall score.
        If the model fails to load, it returns a safe default.
        """
        if self._model is None:
            logger.warning("ML model is not loaded. Returning fallback score 0.0")
            return 0.0, {}

        # Enforce exact feature order used during training
        feature_order = [
            "solar_irradiance_kwh", 
            "wind_speed_ms", 
            "slope_deg", 
            "dist_grid_km", 
            "dist_road_km"
        ]
        
        try:
            # Extract features, defaulting to 0.0 if missing
            input_array = [float(features.get(f, 0.0)) for f in feature_order]
            
            # Model expects 2D array: reshape(1, -1)
            X = np.array(input_array).reshape(1, -1)
            
            # Predict
            prediction = self._model.predict(X)[0]
            
            # Get feature importance if available
            feature_importance = {}
            if hasattr(self._model, 'feature_importances_'):
                importances = self._model.feature_importances_
                # Sort by importance descending
                sorted_idx = np.argsort(importances)[::-1]
                for idx in sorted_idx:
                    feature_importance[feature_order[idx]] = round(float(importances[idx]), 4)
                    
            # Clip between 0 and 100 just in case
            return max(0.0, min(100.0, float(prediction))), feature_importance
            
        except Exception as e:
            logger.error(f"Error during ML prediction: {e}")
            return 0.0, {}

# Export a single global instance
ml_engine = MLInferenceEngine()
