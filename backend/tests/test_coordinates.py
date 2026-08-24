from app.utils.coordinates import validate_latitude
def test_invalid_latitude():
    assert validate_latitude(120) is False