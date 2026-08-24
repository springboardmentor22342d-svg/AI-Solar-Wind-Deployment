from backend.app.feasibility.soft_scoring import SoftConstraintScorer


def test_soft_constraint_scoring():

    features = {
        "distance_to_grid": 6,
        "distance_to_road": 2,
        "solar_irradiance": 5.5,
        "wind_speed": 6.8
    }

    scorer = SoftConstraintScorer()

    score = scorer.calculate_score(features)

    print("\nSoft Feasibility Score:", score)

    assert 0 <= score <= 100


def test_poor_accessibility_reduces_score():

    good_site = {
        "distance_to_grid": 5,
        "distance_to_road": 2,
        "solar_irradiance": 5.5,
        "wind_speed": 6.8
    }

    poor_access_site = {
        "distance_to_grid": 18,
        "distance_to_road": 9,
        "solar_irradiance": 5.5,
        "wind_speed": 6.8
    }

    scorer = SoftConstraintScorer()

    good_score = scorer.calculate_score(good_site)
    poor_score = scorer.calculate_score(poor_access_site)

    print("\nGood site:", good_score)
    print("Poor accessibility site:", poor_score)

    assert poor_score < good_score