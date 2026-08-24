from dataclasses import dataclass
@dataclass
class Coordinate:
    latitude: float
    longitude: float
def validate_latitude(latitude: float) -> bool:
    return -90 <= latitude <= 90
def validate_longitude(longitude: float) -> bool:
    return -180 <= longitude <= 180
def create_coordinate(latitude: float,longitude: float) -> Coordinate:
    if not validate_latitude(latitude):
        raise ValueError("Invalid latitude")
    if not validate_longitude(longitude):
        raise ValueError("Invalid longitude")
    return Coordinate(latitude,longitude)
