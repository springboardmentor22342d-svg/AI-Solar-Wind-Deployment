from backend.app.optimization.deployment_plan import DeploymentPlanGenerator
generator = DeploymentPlanGenerator()


def test_generate_plan():

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
    assert "optimization_remarks" in result
    