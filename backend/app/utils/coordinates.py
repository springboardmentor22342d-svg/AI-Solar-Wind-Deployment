"""
Coordinate validation and a reusable Coordinate object.
"""
from dataclasses import dataclass


class InvalidCoordinateError(ValueError):
    pass


def validate_latitude(latitude: float) -> bool:
    return -90 <= latitude <= 90


def validate_longitude(longitude: float) -> bool:
    return -180 <= longitude <= 180


@dataclass
class Coordinate:
    latitude: float
    longitude: float

    def __post_init__(self):
        if not validate_latitude(self.latitude):
            raise InvalidCoordinateError(f"Invalid latitude: {self.latitude}")
        if not validate_longitude(self.longitude):
            raise InvalidCoordinateError(f"Invalid longitude: {self.longitude}")