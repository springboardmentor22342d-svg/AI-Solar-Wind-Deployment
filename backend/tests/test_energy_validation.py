from backend.app.energy.solar_estimation import (
    estimate_annual_solar_energy
)

from backend.app.energy.wind_estimation import (
    estimate_annual_wind_energy
)

from backend.app.services.energy_estimation_service import (
    EnergyEstimationService
)


def test_higher_capacity_factor_produces_higher_solar_energy():

    low_capacity_factor = estimate_annual_solar_energy(
        installed_capacity=100,
        capacity_factor=0.20
    )

    high_capacity_factor = estimate_annual_solar_energy(
        installed_capacity=100,
        capacity_factor=0.30
    )

    assert high_capacity_factor > low_capacity_factor


def test_higher_capacity_factor_produces_higher_wind_energy():

    low_capacity_factor = estimate_annual_wind_energy(
        installed_capacity=100,
        capacity_factor=0.25
    )

    high_capacity_factor = estimate_annual_wind_energy(
        installed_capacity=100,
        capacity_factor=0.40
    )

    assert high_capacity_factor > low_capacity_factor


def test_hybrid_site_combines_solar_and_wind_energy():

    service = EnergyEstimationService()

    result = service.estimate_energy(
        site_evaluation_result={
            "solar_score": 85,
            "wind_score": 85
        },
        deployment_type="Hybrid",
        installed_capacity=100
    )

    solar_energy = result[
        "estimated_annual_solar_energy_mwh"
    ]

    wind_energy = result[
        "estimated_annual_wind_energy_mwh"
    ]

    total_energy = result[
        "total_estimated_annual_energy_mwh"
    ]

    assert solar_energy > 0

    assert wind_energy > 0

    assert total_energy == solar_energy + wind_energy


def test_estimation_scales_with_capacity():

    service = EnergyEstimationService()

    small_site = service.estimate_energy(
        site_evaluation_result={},
        deployment_type="Solar",
        installed_capacity=50
    )

    large_site = service.estimate_energy(
        site_evaluation_result={},
        deployment_type="Solar",
        installed_capacity=100
    )

    assert (
        large_site[
            "total_estimated_annual_energy_mwh"
        ]
        >
        small_site[
            "total_estimated_annual_energy_mwh"
        ]
    )


def test_three_sample_sites():

    service = EnergyEstimationService()

    solar_site = service.estimate_energy(
        site_evaluation_result={
            "solar_score": 90,
            "wind_score": 40
        },
        deployment_type="Solar",
        installed_capacity=100
    )

    wind_site = service.estimate_energy(
        site_evaluation_result={
            "solar_score": 40,
            "wind_score": 90
        },
        deployment_type="Wind",
        installed_capacity=100
    )

    hybrid_site = service.estimate_energy(
        site_evaluation_result={
            "solar_score": 85,
            "wind_score": 85
        },
        deployment_type="Hybrid",
        installed_capacity=100
    )

    assert solar_site[
        "estimated_annual_solar_energy_mwh"
    ] == 175200

    assert wind_site[
        "estimated_annual_wind_energy_mwh"
    ] == 306600

    assert hybrid_site[
        "total_estimated_annual_energy_mwh"
    ] == 240900