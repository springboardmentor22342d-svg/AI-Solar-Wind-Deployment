from backend.app.services.deployment_strategy import (
    DeploymentStrategyService
)


def test_hybrid_recommendation():

    service = DeploymentStrategyService()

    result = service.generate_recommendation(
        solar_class="Excellent",
        wind_class="Excellent"
    )

    assert result == {
        "deployment": "Hybrid",
        "confidence": 95,
        "reason": "High solar irradiance and consistently strong wind resource."
    }


def test_solar_recommendation():

    service = DeploymentStrategyService()

    result = service.generate_recommendation(
        solar_class="Excellent",
        wind_class="Poor"
    )

    assert result["deployment"] == "Solar"


def test_wind_recommendation():

    service = DeploymentStrategyService()

    result = service.generate_recommendation(
        solar_class="Poor",
        wind_class="Excellent"
    )

    assert result["deployment"] == "Wind"


def test_not_recommended():

    service = DeploymentStrategyService()

    result = service.generate_recommendation(
        solar_class="Poor",
        wind_class="Poor"
    )

    assert result["deployment"] == "Not Recommended"