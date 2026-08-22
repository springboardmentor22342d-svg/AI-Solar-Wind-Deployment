from fastapi import APIRouter, Request, Query, Depends
from app.services.deployment_strategy import build_deployment_recommendation
from app.services.solar_assessment import classify_solar_site
from app.services.wind_assessment import calculate_wind_class, classify_wind_site
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/deployment/recommend")
def get_deployment_recommendation(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    current_user: User = Depends(get_current_user),
):
    builder = request.app.state.feature_builder
    features = builder.build(latitude, longitude)

    solar_irradiance = features.get("solar_irradiance")
    wind_speed = features.get("wind_speed_100m")

    recommendation = build_deployment_recommendation(solar_irradiance, wind_speed)
    wind_details = classify_wind_site(wind_speed)

    return {
        "latitude": latitude,
        "longitude": longitude,
        "solar_irradiance": solar_irradiance,
        "solar_class": classify_solar_site(solar_irradiance),
        "wind_speed": wind_speed,
        "wind_class": wind_details["wind_class"],
        "estimated_wind_capacity_factor_pct": wind_details["estimated_capacity_factor_pct"],
        **recommendation,
    }