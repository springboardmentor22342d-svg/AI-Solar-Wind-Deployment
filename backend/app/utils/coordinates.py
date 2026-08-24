from dataclasses import dataclass


@dataclass(frozen=True)
class Coordinates:
    latitude: float
    longitude: float


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate latitude and longitude ranges.

    Latitude: -90 to 90
    Longitude: -180 to 180
    """

    if not -90 <= latitude <= 90:
        raise ValueError("Latitude must be between -90 and 90")

    if not -180 <= longitude <= 180:
        raise ValueError("Longitude must be between -180 and 180")

    return True


def create_coordinates(latitude: float, longitude: float) -> Coordinates:
    """
    Validate coordinates and return a reusable Coordinates object.
    """

    validate_coordinates(latitude, longitude)

    return Coordinates(
        latitude=latitude,
        longitude=longitude
    )