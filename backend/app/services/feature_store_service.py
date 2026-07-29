from sqlalchemy.orm import Session
from app.models.feature import Feature
from app.schemas.feature import FeatureCreate

class FeatureStoreService:
    """
    Handles persistence and retrieval of feature records.
    Pure database operations — does not call FeatureBuilder or any
    external data source directly (that integration happens elsewhere).
    """

    def __init__(self, db: Session):
        self.db = db

    def save(self, feature: FeatureCreate) -> Feature:
        new_feature = Feature(**feature.model_dump())
        self.db.add(new_feature)
        self.db.commit()
        self.db.refresh(new_feature)
        return new_feature

    def get_all(self) -> list[Feature]:
        return self.db.query(Feature).all()

    def get_by_id(self, feature_id: int) -> Feature | None:
        return self.db.query(Feature).filter(Feature.id == feature_id).first()

    def find_by_coordinates(self, latitude: float, longitude: float, tolerance: float = 0.001) -> Feature | None:
        """
        Cache lookup — checks if a feature record already exists for
        approximately this coordinate, to avoid recomputing.
        """
        return (
            self.db.query(Feature)
            .filter(Feature.latitude.between(latitude - tolerance, latitude + tolerance))
            .filter(Feature.longitude.between(longitude - tolerance, longitude + tolerance))
            .first()
        )