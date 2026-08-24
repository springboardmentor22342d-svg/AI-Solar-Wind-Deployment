
from backend.app.energy_yield.energy_yield_service import EnergyYieldService


def test_higher_solar_irradiance_produces_higher_energy():

    service = EnergyYieldService()

    low_solar = service.estimate_solar_energy(
        installed_capacity_mw=10,
        solar_irradiance=3.5
    )

    high_solar = service.estimate_solar_energy(
        installed_capacity_mw=10,
        solar_irradiance=6.0
    )

    print("\nLow Solar Energy:", low_solar)
    print("High Solar Energy:", high_solar)

    assert high_solar["annual_energy_mwh"] > \
           low_solar["annual_energy_mwh"]


def test_higher_wind_speed_produces_higher_energy():

    service = EnergyYieldService()

    low_wind = service.estimate_wind_energy(
        installed_capacity_mw=10,
        wind_speed=4.0
    )

    high_wind = service.estimate_wind_energy(
        installed_capacity_mw=10,
        wind_speed=8.0
    )

    print("\nLow Wind Energy:", low_wind)
    print("High Wind Energy:", high_wind)

    assert high_wind["annual_energy_mwh"] > \
           low_wind["annual_energy_mwh"]


def test_higher_capacity_factor_produces_higher_energy():

    service = EnergyYieldService()

    low_capacity_factor = service.estimate_annual_energy(
        installed_capacity_mw=10,
        capacity_factor=0.25,
        system_efficiency=0.90,
        operational_losses=0.10
    )

    high_capacity_factor = service.estimate_annual_energy(
        installed_capacity_mw=10,
        capacity_factor=0.50,
        system_efficiency=0.90,
        operational_losses=0.10
    )

    print("\nLow Capacity Factor:", low_capacity_factor)
    print("High Capacity Factor:", high_capacity_factor)

    assert high_capacity_factor["annual_energy_mwh"] > \
           low_capacity_factor["annual_energy_mwh"]


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

    print("\nHybrid Energy:", result)

    assert result["total_annual_energy_mwh"] == expected
