from dataclasses import dataclass

@dataclass
class Coordinate:
    latitude: float
    longitude: float

    def __post_init__(self):
        if not (-90 <= self.latitude <= 90):
            raise ValueError(f"Invalid latitude: {self.latitude}. Must be between -90 and 90.")
        if not (-180 <= self.longitude <= 180):
            raise ValueError(f"Invalid longitude: {self.longitude}. Must be between -180 and 180.")

def validate_coordinates(lat: float, lon: float) -> bool:
    """Validates if the given latitude and longitude are within valid ranges."""
    return (-90 <= lat <= 90) and (-180 <= lon <= 180)

def create_coordinate(lat: float, lon: float) -> Coordinate:
    """Converts latitude and longitude into a reusable Coordinate object."""
    return Coordinate(latitude=lat, longitude=lon)
