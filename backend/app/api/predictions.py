from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List

from app.ml.model_inference import ModelInference
from app.ml.feature_importance import FeatureImportance
from app.services.training_service import TrainingService

router = APIRouter(
    prefix="/predictions",
    tags=["Predictions"]
)

inference_engine = None
feature_importance_engine = None

try:
    inference_engine = ModelInference()
    feature_importance_engine = FeatureImportance()
except Exception as err:
    print(f"Prediction router init notice: {err}")


class FeatureInputSchema(BaseModel):
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)
    day_of_year: int = Field(..., ge=1, le=366)
    week_of_year: int = Field(..., ge=1, le=53)
    temperature: float
    humidity: float = Field(..., ge=0, le=100)
    wind_speed: float = Field(..., ge=0)


@router.post("/predict")
def predict_solar_output(features: FeatureInputSchema):
    """
    Predict solar irradiance using the trained Random Forest ML model.
    """
    if not inference_engine:
        raise HTTPException(status_code=500, detail="ML Model inference engine is not loaded.")

    try:
        feature_list = [
            features.month,
            features.day,
            features.day_of_year,
            features.week_of_year,
            features.temperature,
            features.humidity,
            features.wind_speed,
        ]
        predicted_value = inference_engine.predict(feature_list)
        
        explainability = []
        if feature_importance_engine:
            explainability = feature_importance_engine.get_feature_importance()[:3]

        return {
            "success": True,
            "predicted_solar_irradiance": round(predicted_value, 4),
            "unit": "kWh/m²/day",
            "top_explaining_features": explainability,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.get("/feature-importance")
def get_feature_importance():
    """
    Retrieve feature importance weights of the trained ML model.
    """
    if not feature_importance_engine:
        raise HTTPException(status_code=500, detail="Feature importance engine unavailable.")
    
    return {
        "success": True,
        "feature_rankings": feature_importance_engine.get_feature_importance()
    }


@router.post("/train")
def train_model():
    """
    Train/Retrain the Random Forest solar prediction model.
    """
    try:
        service = TrainingService()
        result = service.train()
        return {
            "success": True,
            "message": "Model trained and saved successfully.",
            "metrics": result["metrics"],
            "model_path": result["model_path"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training error: {str(e)}")