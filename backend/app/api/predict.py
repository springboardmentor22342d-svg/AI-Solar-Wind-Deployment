from fastapi import APIRouter
from app.services.model_service import ModelService
from app.schemas.analysis_response import AnalysisResponse


router = APIRouter(
    prefix="/predict",
    tags=["Prediction"]
)


service = ModelService()


@router.post(
    "",
    response_model=AnalysisResponse
)
def predict(
    wind_speed: float,
    temperature: float,
    humidity: float,
    date: str
):

    result = service.predict(
        wind_speed=wind_speed,
        temperature=temperature,
        humidity=humidity,
        date=date
    )

    return result