"""
Orchestrates energy estimation for a site, based on its deployment
recommendation (Solar / Wind / Hybrid) and installed capacity.
"""

from app.services.energy_estimation import (
    estimate_solar_annual_energy,
    estimate_wind_annual_energy,
    is_profitable,
)


def estimate_site_energy(features: dict, deployment_type: str, installed_capacity_kw: float,
                          hybrid_split: float = 0.5) -> dict:
    """
    Input:
        features: dict with at least solar_irradiance, wind_speed_100m
        deployment_type: "Solar", "Wind", or "Hybrid"
        installed_capacity_kw: total planned capacity
        hybrid_split: for Hybrid sites, fraction of capacity assigned
            to solar (remainder goes to wind). Default 50/50.

    Output: solar/wind/total annual energy estimates + profitability flag.
    """
    solar_irradiance = features.get("solar_irradiance")
    wind_speed = features.get("wind_speed_100m")

    solar_result = {"capacity_factor_pct": 0.0, "annual_energy_kwh": 0.0}
    wind_result = {"capacity_factor_pct": 0.0, "annual_energy_kwh": 0.0}

    if deployment_type == "Solar":
        solar_result = estimate_solar_annual_energy(installed_capacity_kw, solar_irradiance)

    elif deployment_type == "Wind":
        wind_result = estimate_wind_annual_energy(installed_capacity_kw, wind_speed)

    elif deployment_type == "Hybrid":
        solar_capacity = installed_capacity_kw * hybrid_split
        wind_capacity = installed_capacity_kw * (1 - hybrid_split)
        solar_result = estimate_solar_annual_energy(solar_capacity, solar_irradiance)
        wind_result = estimate_wind_annual_energy(wind_capacity, wind_speed)

    total_energy_kwh = solar_result["annual_energy_kwh"] + wind_result["annual_energy_kwh"]

    return {
        "deployment_type": deployment_type,
        "estimated_annual_solar_energy_kwh": solar_result["annual_energy_kwh"],
        "estimated_annual_wind_energy_kwh": wind_result["annual_energy_kwh"],
        "total_estimated_annual_energy_kwh": total_energy_kwh,
        "is_profitable": is_profitable(total_energy_kwh),
        "minimum_viable_threshold_kwh": 500_000,
    }