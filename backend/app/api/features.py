from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.feature import (
    FeatureCreate,
    FeatureResponse
)

from app.services.feature_store_service import (
    FeatureStoreService
)

router = APIRouter(
    prefix="/features",
    tags=["Features"]
)

service = FeatureStoreService()


@router.post(
    "",
    response_model=FeatureResponse
)
def create_feature(
    feature: FeatureCreate,
    db: Session = Depends(get_db)
):

    return service.create_feature(
        db,
        feature
    )


@router.get(
    "",
    response_model=list[FeatureResponse]
)
def get_all_features(
    db: Session = Depends(get_db)
):

    return service.get_all_features(db)


@router.get(
    "/{feature_id}",
    response_model=FeatureResponse
)
def get_feature(
    feature_id: int,
    db: Session = Depends(get_db)
):

    feature = service.get_feature_by_id(
        db,
        feature_id
    )

    if feature is None:

        raise HTTPException(
            status_code=404,
            detail="Feature not found"
        )

    return feature


@router.delete("/{feature_id}")
def delete_feature(
    feature_id: int,
    db: Session = Depends(get_db)
):

    feature = service.delete_feature(
        db,
        feature_id
    )

    if feature is None:

        raise HTTPException(
            status_code=404,
            detail="Feature not found"
        )

    return {

        "message": "Feature deleted successfully."

    }