from fastapi import APIRouter
from app.services.solar_services import SolarFeatureService
router = APIRouter(prefix="/solar",tags=["Solar"])

service = SolarFeatureService()

@router.get("/features")
def get_solar_features(latitude: float,longitude: float):
    return service.get_features(latitude,longitude)