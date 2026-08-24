from backend.app.services.energy_estimation_service import (
    EnergyEstimationService
)


def test_solar_energy_estimation():

    service = EnergyEstimationService()

    result = service.estimate_energy(
        site_evaluation_result={
            "solar_score": 85,
            "wind_score": 50
        },
        deployment_type="Solar",
        installed_capacity=100
    )

    assert result[
        "estimated_annual_solar_energy_mwh"
    ] == 175200

    assert result[
        "estimated_annual_wind_energy_mwh"
    ] == 0

    assert result[
        "total_estimated_annual_energy_mwh"
    ] == 175200


def test_wind_energy_estimation():

    service = EnergyEstimationService()

    result = service.estimate_energy(
        site_evaluation_result={
            "solar_score": 50,
            "wind_score": 85
        },
        deployment_type="Wind",
        installed_capacity=100
    )

    assert result[
        "estimated_annual_solar_energy_mwh"
    ] == 0

    assert result[
        "estimated_annual_wind_energy_mwh"
    ] == 306600

    assert result[
        "total_estimated_annual_energy_mwh"
    ] == 306600


def test_hybrid_energy_estimation():

    service = EnergyEstimationService()

    result = service.estimate_energy(
        site_evaluation_result={
            "solar_score": 85,
            "wind_score": 85
        },
        deployment_type="Hybrid",
        installed_capacity=100
    )

    assert result[
        "estimated_annual_solar_energy_mwh"
    ] == 87600

    assert result[
        "estimated_annual_wind_energy_mwh"
    ] == 153300

    assert result[
        "total_estimated_annual_energy_mwh"
    ] == 240900