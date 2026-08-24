from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.app.inference.model_inference import ModelInference


router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


class PredictionRequest(BaseModel):
    temperature: float
    humidity: float
    wind_speed: float
    solar_irradiance: float
    year: int
    month: int
    day: int
    day_of_year: int
    


model = ModelInference(
    "models/best_model.pkl"
)


@router.post("/")
def predict(request: PredictionRequest):

    try:

        features = {
            "temperature": request.temperature,
            "humidity": request.humidity,
            "wind_speed": request.wind_speed,
            "solar_irradiance": request.solar_irradiance,
            "year": request.year,
            "month": request.month,
            "day": request.day,
            "day_of_year": request.day_of_year,
            
        }

        prediction = model.predict(
            features
        )

        return {
            "prediction": prediction
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )