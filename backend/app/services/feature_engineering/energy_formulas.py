import math

# ---- Solar constants (India, utility-scale crystalline-silicon PV) ----
PANEL_EFFICIENCY = 0.18           # 18%, typical commercial panel
PERFORMANCE_RATIO = 0.75          # accounts for temperature, wiring, inverter, soiling losses
REFERENCE_AREA_M2 = 10_000        # 1 hectare reference plot, for comparable per-site output

# ---- Wind constants (India, typical utility-scale turbine class) ----
ROTOR_DIAMETER_M = 100
SWEPT_AREA_M2 = math.pi * (ROTOR_DIAMETER_M / 2) ** 2   # ≈ 7854 m²
POWER_COEFFICIENT = 0.40           # Cp, realistic modern turbine value (Betz limit = 0.593)
AIR_DENSITY_SEA_LEVEL = 1.225      # kg/m³, standard sea-level value
CUT_IN_SPEED = 3.0                 # m/s — below this, turbine produces zero power
CUT_OUT_SPEED = 25.0               # m/s — above this, turbine shuts down for safety


def estimate_solar_energy_kwh_per_year(ghi: float) -> float | None:
    """
    Estimates annual solar energy output (kWh/year) for a reference
    1-hectare installation, using the standard formula:
        E = A * r * H * PR
    where H (annual radiation, kWh/m²/year) is derived from daily GHI
    (kWh/m²/day, as provided by NASA POWER) * 365.
    """
    if ghi is None:
        return None
    annual_irradiation = ghi * 365  # kWh/m²/year
    energy = REFERENCE_AREA_M2 * PANEL_EFFICIENCY * annual_irradiation * PERFORMANCE_RATIO
    return round(energy, 2)


def _air_density_at_elevation(elevation_m: float) -> float:
    """
    Adjusts standard sea-level air density for site elevation.
    Approximation: air density drops ~3.5% per 305m (1000ft) of elevation.
    """
    if elevation_m is None:
        return AIR_DENSITY_SEA_LEVEL
    reduction_factor = 0.035 * (elevation_m / 305)
    return AIR_DENSITY_SEA_LEVEL * max(0.5, 1 - reduction_factor)  # floor to avoid unrealistic values


def estimate_wind_energy_kwh_per_year(wind_speed_100m: float, elevation: float = None) -> float | None:
    """
    Estimates annual wind energy output (kWh/year) for a single turbine,
    using the standard formula:
        P = 0.5 * rho * A * v^3 * Cp
    Applies cut-in/cut-out speed limits, and adjusts air density for
    site elevation using the district elevation feature.
    """
    if wind_speed_100m is None:
        return None
    if wind_speed_100m < CUT_IN_SPEED or wind_speed_100m > CUT_OUT_SPEED:
        return 0.0

    rho = _air_density_at_elevation(elevation)
    power_watts = 0.5 * rho * SWEPT_AREA_M2 * (wind_speed_100m ** 3) * POWER_COEFFICIENT
    power_kw = power_watts / 1000
    annual_energy_kwh = power_kw * 8760  # hours in a year
    return round(annual_energy_kwh, 2)