from fastapi import APIRouter, Request, Query, Depends
from app.optimization.deployment_plan import generate_deployment_plan
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/optimization/plan")
def get_optimization_plan(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    land_area_hectares: float = Query(..., gt=0),
    grid_capacity_limit_mw: float = Query(None),
    current_user: User = Depends(get_current_user),
):
    builder = request.app.state.feature_builder
    features = builder.build(latitude, longitude)

    plan = generate_deployment_plan(features, land_area_hectares, grid_capacity_limit_mw)
    plan["latitude"] = latitude
    plan["longitude"] = longitude
    return plan