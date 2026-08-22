from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.services.feature_store_service import FeatureStoreService
from app.schemas.feature import FeatureCreate, FeatureResponse
from app.auth.security import require_role
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()


# ---- Live computation (via FeatureBuilder, no database involved) ----
@router.get("/features/compute")
def compute_features(
    request: Request,
    latitude: float = Query(..., ge=-90, le=90),
    longitude: float = Query(..., ge=-180, le=180),
    current_user: User = Depends(get_current_user),
):
    builder = request.app.state.feature_builder
    return builder.build(latitude, longitude)


# ---- Stored feature records (Feature Store / database) ----
@router.post("/features", response_model=FeatureResponse)
def create_feature(feature: FeatureCreate, db: Session = Depends(get_db)):
    service = FeatureStoreService(db)
    return service.save(feature)

@router.get("/features", response_model=list[FeatureResponse])
def get_all_features(db: Session = Depends(get_db), skip: int = 0, limit: int = 50,
                      current_user: User = Depends(require_role(["Administrator", "GIS Analyst"]))):
    service = FeatureStoreService(db)
    return service.get_all(skip=skip, limit=limit)

@router.get("/features/{feature_id}", response_model=FeatureResponse)
def get_feature_by_id(feature_id: int, db: Session = Depends(get_db)):
    service = FeatureStoreService(db)
    feature = service.get_by_id(feature_id)
    if not feature:
        raise HTTPException(status_code=404, detail="Feature not found")
    return feature