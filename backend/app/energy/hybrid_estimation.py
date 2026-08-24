from backend.app.energy.solar_estimation import (
    estimate_annual_solar_energy
)

from backend.app.energy.wind_estimation import (
    estimate_annual_wind_energy
)


def estimate_annual_hybrid_energy(
    solar_capacity: float,
    wind_capacity: float,
    solar_capacity_factor: float,
    wind_capacity_factor: float
) -> dict:
    """
    Estimate combined annual energy generation
    from solar and wind sources.
    """

    solar_energy = estimate_annual_solar_energy(
        installed_capacity=solar_capacity,
        capacity_factor=solar_capacity_factor
    )

    wind_energy = estimate_annual_wind_energy(
        installed_capacity=wind_capacity,
        capacity_factor=wind_capacity_factor
    )

    total_energy = solar_energy + wind_energy

    return {
        "estimated_annual_solar_energy_mwh": solar_energy,
        "estimated_annual_wind_energy_mwh": wind_energy,
        "total_estimated_annual_energy_mwh": total_energy
    }