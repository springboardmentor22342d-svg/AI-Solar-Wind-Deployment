from fastapi import APIRouter

from app.services.feature_engineering.solar import SolarFeatureEngineering

router = APIRouter(
    prefix="/solar",
    tags=["Solar"]
)

solar_service = SolarFeatureEngineering()


@router.get("/features")
def get_solar_features(
    latitude: float,
    longitude: float,
):
    """
    Fetch solar features from NASA POWER API.
    """

    return solar_service.build_features(
        latitude,
        longitude,
    )