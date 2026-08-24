from fastapi import APIRouter, HTTPException, Query

from backend.app.services.feature_engineering.solar import SolarService


router = APIRouter(
    prefix="/solar",
    tags=["Solar"]
)

solar_service = SolarService()


@router.get("/features")
def get_solar_features(
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180)
):
    data = solar_service.get_solar_data(
        latitude=latitude,
        longitude=longitude
    )

    if data is None:
        raise HTTPException(
            status_code=503,
            detail="NASA POWER service is currently unavailable."
        )

    return data