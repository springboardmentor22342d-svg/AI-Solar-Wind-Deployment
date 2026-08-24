

from backend.app.optimization.deployment_plan import DeploymentPlanGenerator

generator = DeploymentPlanGenerator()


def test_hybrid_site():
    site = {
        "solar_score": 90,
        "wind_score": 88,
        "overall_score": 90,
        "land_area": 250
    }

    result = generator.generate_plan(site)

    assert result["recommended_technology"] == "Hybrid"
    assert result["recommended_capacity"] == "100 MW"
    assert result["expansion_status"] == "Expandable"


def test_solar_site():
    site = {
        "solar_score": 86,
        "wind_score": 60,
        "overall_score": 78,
        "land_area": 120
    }

    result = generator.generate_plan(site)

    assert result["recommended_technology"] == "Solar"
    assert result["recommended_capacity"] == "50 MW"
    assert result["expansion_status"] == "Limited Expansion"


def test_wind_site():
    site = {
        "solar_score": 60,
        "wind_score": 84,
        "overall_score": 76,
        "land_area": 80
    }

    result = generator.generate_plan(site)

    assert result["recommended_technology"] == "Wind"
    assert result["recommended_capacity"] == "25 MW"
    assert result["expansion_status"] == "Not Expandable"


def test_small_site():
    site = {
        "solar_score": 70,
        "wind_score": 65,
        "overall_score": 60,
        "land_area": 15
    }

    result = generator.generate_plan(site)

    assert result["recommended_capacity"] == "5 MW"
    assert result["expansion_status"] == "Not Expandable"

    