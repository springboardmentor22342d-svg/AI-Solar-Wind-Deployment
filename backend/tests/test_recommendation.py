from backend.app.evaluation.recommendation import (
    get_recommendation
)


def test_highly_suitable_recommendation():
    assert get_recommendation(85) == "Highly Suitable"


def test_suitable_recommendation():
    assert get_recommendation(70) == "Suitable"


def test_moderately_suitable_recommendation():
    assert get_recommendation(50) == "Moderately Suitable"


def test_not_recommended():
    assert get_recommendation(49) == "Not Recommended"