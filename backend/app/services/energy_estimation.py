"""
Annual energy estimation, using the standard engineering formula:
    Annual Energy (kWh) = Installed Capacity (kW) × Capacity Factor × Operating Hours (8760)
"""

from app.services.solar_assessment import calculate_solar_capacity_factor
from app.services.wind_assessment import calculate_capacity_factor as calculate_wind_capacity_factor

OPERATING_HOURS_PER_YEAR = 8760

# Simplified profitability indicator — NOT a real financial model
# (no cost-per-kWh, capex, or tariff data available). Flags whether
# a site's estimated output clears a minimum viable production
# threshold, so viable sites aren't approved purely on suitability
# score while producing too little energy to be worthwhile.
MINIMUM_VIABLE_ANNUAL_ENERGY_KWH = 500_000  # ~500 MWh/year, adjustable


def calculate_annual_energy_kwh(installed_capacity_kw: float, capacity_factor_pct: float,
                                 operating_hours: int = OPERATING_HOURS_PER_YEAR) -> float:
    """Generic reusable formula — works for solar, wind, or any generation type."""
    if installed_capacity_kw is None or capacity_factor_pct is None:
        return 0.0
    return round(installed_capacity_kw * (capacity_factor_pct / 100) * operating_hours, 2)


def estimate_solar_annual_energy(installed_capacity_kw: float, solar_irradiance: float) -> dict:
    capacity_factor = calculate_solar_capacity_factor(solar_irradiance)
    energy_kwh = calculate_annual_energy_kwh(installed_capacity_kw, capacity_factor)
    return {"capacity_factor_pct": capacity_factor, "annual_energy_kwh": energy_kwh}


def estimate_wind_annual_energy(installed_capacity_kw: float, wind_speed: float) -> dict:
    capacity_factor = calculate_wind_capacity_factor(wind_speed)
    energy_kwh = calculate_annual_energy_kwh(installed_capacity_kw, capacity_factor)
    return {"capacity_factor_pct": capacity_factor, "annual_energy_kwh": energy_kwh}


def is_profitable(total_annual_energy_kwh: float) -> bool:
    """Simplified check: does this site clear the minimum viable production threshold?"""
    if total_annual_energy_kwh is None:
        return False
    return total_annual_energy_kwh >= MINIMUM_VIABLE_ANNUAL_ENERGY_KWH