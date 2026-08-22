from fastapi import APIRouter, Request, Query, Depends
from app.services.energy_estimation_service import estimate_site_energy
from app.services.deployment_strategy import build_deployment_recommendation
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/energy/estimate")
def get_energy_estimate(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    installed_capacity_kw: float = Query(..., gt=0),
    current_user: User = Depends(get_current_user),
):
    builder = request.app.state.feature_builder
    features = builder.build(latitude, longitude)

    solar_irradiance = features.get("solar_irradiance")
    wind_speed = features.get("wind_speed_100m")
    deployment_type = build_deployment_recommendation(solar_irradiance, wind_speed)["deployment"]

    result = estimate_site_energy(features, deployment_type, installed_capacity_kw)
    result["latitude"] = latitude
    result["longitude"] = longitude
    return result