
import pytest

from backend.app.energy_yield.energy_yield_service import EnergyYieldService


def test_solar_energy_estimation():

    service = EnergyYieldService()

    result = service.estimate_solar_energy(
        installed_capacity_mw=10,
        solar_irradiance=5.5
    )

    print("\nSolar Energy:")
    print(result)

    assert result["technology"] == "Solar"
    assert result["solar_irradiance"] == 5.5
    assert result["annual_energy_mwh"] > 0
    assert result["annual_energy_gwh"] > 0


def test_wind_energy_estimation():

    service = EnergyYieldService()

    result = service.estimate_wind_energy(
        installed_capacity_mw=10,
        wind_speed=6.8
    )

    print("\nWind Energy:")
    print(result)

    assert result["technology"] == "Wind"
    assert result["wind_speed"] == 6.8
    assert result["annual_energy_mwh"] > 0
    assert result["annual_energy_gwh"] > 0


def test_hybrid_energy_estimation():

    service = EnergyYieldService()

    result = service.estimate_hybrid_energy(
        solar_capacity_mw=10,
        wind_capacity_mw=10,
        solar_irradiance=5.5,
        wind_speed=6.8
    )

    print("\nHybrid Energy:")
    print(result)

    assert result["technology"] == "Hybrid"
    assert result["solar"]["annual_energy_mwh"] > 0
    assert result["wind"]["annual_energy_mwh"] > 0
    assert result["total_annual_energy_mwh"] > 0


def test_hybrid_energy_equals_solar_plus_wind():

    service = EnergyYieldService()

    result = service.estimate_hybrid_energy(
        solar_capacity_mw=10,
        wind_capacity_mw=10,
        solar_irradiance=5.5,
        wind_speed=6.8
    )

    expected = (
        result["solar"]["annual_energy_mwh"]
        + result["wind"]["annual_energy_mwh"]
    )

    assert result["total_annual_energy_mwh"] == pytest.approx(expected)





def test_capacity_factor_and_efficiency_are_applied():

    service = EnergyYieldService()

    result = service.estimate_annual_energy(
        installed_capacity_mw=10,
        capacity_factor=0.40,
        system_efficiency=0.90,
        operational_losses=0.10
    )

    expected = (
        10
        * 8760
        * 0.40
        * 0.90
        * (1 - 0.10)
    )

    assert result["annual_energy_mwh"] == pytest.approx(
        expected,
        rel=1e-6
    )

    assert result["annual_energy_gwh"] == pytest.approx(
        round(expected / 1000, 2)
    )
