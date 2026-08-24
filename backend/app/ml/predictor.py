import pandas as pd
from app.ml.model_loader import get_model
class Predictor:
    def predict(self,
                wind_speed,
                temperature,
                humidity,
                date):
        date = pd.to_datetime(date)
        features = pd.DataFrame([{
            "wind_speed": wind_speed,
            "temperature": temperature,
            "humidity": humidity,
            "year": date.year,
            "month": date.month,
            "day": date.day,
            "day_of_year": date.dayofyear
        }])
        model = get_model()

        prediction = model.predict(features)
        importance = model.feature_importances_
        feature_names = list(features.columns)
        importance_list = sorted(
            zip(feature_names,importance),
            key=lambda x: x[1],
            reverse=True
        )
        top_features =[
            item[0]
            for item in importance_list[:3]
        ]
        return {
            "prediction": float(prediction),
            "explanation": "Prediction mainly influenced by: "+",".join(top_features)
        }
"""
Inference & Prediction Orchestration Service.
Uses ProductionPredictor and ModelInferenceModule for single-load cached joblib model management.
"""

from typing import Dict, Any, Optional, Union
import pandas as pd

from app.ml.inference import ModelInferenceModule
from app.ml.prediction import ProductionPredictor
from app.ml.schemas import FeatureVector


class MLPredictor:
    """
    Inference service orchestrator leveraging ProductionPredictor and ModelInferenceModule.
    """

    def __init__(self, models_dir: Optional[str] = None):
        self.inference_module = ModelInferenceModule(models_dir)
        self.predictor = ProductionPredictor(models_dir)

    def get_or_train_model(
        self, prediction_type: str = "regression", db: Any = None, target_col: str = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves cached model artifact from memory or disk if available.
        """
        return self.predictor.load_model()

    def predict(
        self,
        feature_data: Union[Dict[str, Any], FeatureVector, pd.DataFrame],
        prediction_type: str = "regression",
        db: Any = None
    ) -> Dict[str, Any]:
        """
        Executes prediction pipeline via ProductionPredictor.
        """
        return self.predictor.predict(
            feature_data=feature_data,
            prediction_type=prediction_type
        )
