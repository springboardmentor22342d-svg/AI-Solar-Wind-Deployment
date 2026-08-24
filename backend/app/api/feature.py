from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database.database import SessionLocal
from backend.app.schemas.feature import FeatureResponse
from backend.app.services.feature_store import FeatureStoreService

router = APIRouter(
    prefix="",
    tags=["Features"]
)

service = FeatureStoreService()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[FeatureResponse])
def get_features(db: Session = Depends(get_db)):
    return service.get_all_features(db)


@router.get("/{feature_id}", response_model=FeatureResponse)
def get_feature(feature_id: int, db: Session = Depends(get_db)):
    feature = service.get_feature_by_id(db, feature_id)

    if feature is None:
        raise HTTPException(
            status_code=404,
            detail="Feature not found"
        )

    return feature