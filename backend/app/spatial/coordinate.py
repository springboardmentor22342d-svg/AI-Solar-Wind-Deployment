from dataclasses import dataclass


@dataclass
class Coordinate:
    latitude: float
    longitude: float


class CoordinateValidator:

    @staticmethod
    def validate_latitude(latitude: float) -> bool:
        return -90 <= latitude <= 90

    @staticmethod
    def validate_longitude(longitude: float) -> bool:
        return -180 <= longitude <= 180

    @classmethod
    def validate_coordinate(cls, latitude: float, longitude: float) -> bool:
        return (
            cls.validate_latitude(latitude)
            and cls.validate_longitude(longitude)
        )

    @classmethod
    def create_coordinate(cls, latitude: float, longitude: float) -> Coordinate:

        if not cls.validate_coordinate(latitude, longitude):
            raise ValueError("Invalid latitude or longitude.")

        return Coordinate(latitude, longitude)