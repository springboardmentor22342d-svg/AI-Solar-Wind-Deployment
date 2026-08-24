import pytest

from backend.app.evaluation.scorer import (
    calculate_weighted_score
)


def test_weighted_score_is_calculated():

    features = {
        "solar_irradiance": 5.8,
        "wind_speed": 6.2,
        "slope": 2.1,
        "distance_to_grid": 4.0,
        "distance_to_road": 2.0,
    }

    score = calculate_weighted_score(features)

    expected_score = (
        (5.8 * 0.35)
        + (6.2 * 0.25)
        + (2.1 * 0.15)
        + (4.0 * 0.15)
        + (2.0 * 0.10)
    )

    assert score == pytest.approx(expected_score)


def test_missing_feature_raises_error():

    features = {
        "solar_irradiance": 5.8,
        "wind_speed": 6.2,
    }

    with pytest.raises(KeyError):

        calculate_weighted_score(features)