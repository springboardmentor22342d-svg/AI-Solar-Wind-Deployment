from fastapi import APIRouter, Request, Query, HTTPException

router = APIRouter()

@router.get("/solar/features")
def get_solar_features(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
):
    builder = request.app.state.feature_builder
    result = builder.solar_service.get_features(latitude, longitude)

    if all(v is None for v in result.values()):
        raise HTTPException(
            status_code=502,
            detail="Unable to retrieve solar data for this location.",
        )
    return result