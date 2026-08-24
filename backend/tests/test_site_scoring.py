from backend.app.evaluation.category_scoring import (
    calculate_renewable_resource_score,
    calculate_terrain_score,
    calculate_infrastructure_score,
    calculate_environmental_score,
    calculate_economic_score
)

from backend.app.evaluation.overall_scoring import (
    calculate_overall_site_score
)


def test_complete_site_scoring():

    renewable_score = calculate_renewable_resource_score(
        solar_irradiance=5.8,
        wind_speed=6.2
    )

    terrain_score = calculate_terrain_score(
        slope=2.1,
        elevation=540
    )

    infrastructure_score = calculate_infrastructure_score(
        distance_to_road=5,
        distance_to_grid=10
    )

    environmental_score = calculate_environmental_score(
        environmental_sensitivity=20
    )

    economic_score = calculate_economic_score(
        land_cost=30,
        estimated_roi=80
    )

    category_scores = {
        "renewable_resource": renewable_score,
        "terrain": terrain_score,
        "infrastructure": infrastructure_score,
        "environmental": environmental_score,
        "economic": economic_score
    }

    result = calculate_overall_site_score(
        category_scores
    )

    print("\nCATEGORY-WISE SCORING RESULT")
    print("===========================")

    print(
        f"Renewable Resource Score: "
        f"{renewable_score}"
    )

    print(
        f"Terrain Score: "
        f"{terrain_score}"
    )

    print(
        f"Infrastructure Score: "
        f"{infrastructure_score}"
    )

    print(
        f"Environmental Score: "
        f"{environmental_score}"
    )

    print(
        f"Economic Score: "
        f"{economic_score}"
    )

    print("\nOVERALL RESULT")
    print("==============")
    print(
        f"Overall Score: "
        f"{result['overall_score']}"
    )

    print(
        f"Suitability: "
        f"{result['suitability']}"
    )

    assert 0 <= renewable_score <= 100
    assert 0 <= terrain_score <= 100
    assert 0 <= infrastructure_score <= 100
    assert 0 <= environmental_score <= 100
    assert 0 <= economic_score <= 100

    assert 0 <= result["overall_score"] <= 100