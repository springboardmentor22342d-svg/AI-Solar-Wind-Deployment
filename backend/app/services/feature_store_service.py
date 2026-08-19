from sqlalchemy.orm import Session

from app.models.feature import Feature

from app.schemas.feature import FeatureCreate


class FeatureStoreService:

    def create_feature(
        self,
        db: Session,
        feature: FeatureCreate
    ):

        db_feature = Feature(

            latitude=feature.latitude,

            longitude=feature.longitude,

            solar_irradiance=feature.solar_irradiance,

            wind_speed=feature.wind_speed,

            temperature=feature.temperature,

            humidity=feature.humidity,

            elevation=feature.elevation,

            slope=feature.slope,

            distance_to_grid=feature.distance_to_grid,

            distance_to_road=feature.distance_to_road

        )

        db.add(db_feature)

        db.commit()

        db.refresh(db_feature)

        return db_feature

    def get_all_features(
        self,
        db: Session
    ):

        return db.query(Feature).all()

    def get_feature_by_id(
        self,
        db: Session,
        feature_id: int
    ):

        return (

            db.query(Feature)

            .filter(

                Feature.id == feature_id

            )

            .first()

        )

    def get_feature_by_location(
        self,
        db: Session,
        latitude: float,
        longitude: float
    ):

        return (

            db.query(Feature)

            .filter(

                Feature.latitude == latitude,

                Feature.longitude == longitude

            )

            .first()

        )

    def delete_feature(
        self,
        db: Session,
        feature_id: int
    ):

        feature = (

            db.query(Feature)

            .filter(

                Feature.id == feature_id

            )

            .first()

        )

        if feature:

            db.delete(feature)

            db.commit()

        return feature