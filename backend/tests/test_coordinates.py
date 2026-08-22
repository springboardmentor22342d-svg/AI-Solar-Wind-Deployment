import pytest
from app.utils.coordinates import Coordinate, InvalidCoordinateError


def test_valid_coordinate():
    c = Coordinate(latitude=23.26, longitude=77.41)
    assert c.latitude == 23.26

def test_invalid_latitude_too_high():
    with pytest.raises(InvalidCoordinateError):
        Coordinate(latitude=200, longitude=77.41)

def test_invalid_latitude_too_low():
    with pytest.raises(InvalidCoordinateError):
        Coordinate(latitude=-200, longitude=77.41)

def test_invalid_longitude_too_high():
    with pytest.raises(InvalidCoordinateError):
        Coordinate(latitude=23.26, longitude=400)

def test_invalid_longitude_too_low():
    with pytest.raises(InvalidCoordinateError):
        Coordinate(latitude=23.26, longitude=-400)