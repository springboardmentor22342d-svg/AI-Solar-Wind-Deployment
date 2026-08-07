"""
Energy Yield Service — solar/wind/hybrid annual energy estimation.
Uses trained ML predictions where available (see ml_prediction_service.py),
falling back to the rule-based engineering formula
(Installed Capacity x Capacity Factor x 8760 x System Efficiency)
when ML prediction is unavailable — ensuring the service never
returns a purely theoretical value with no grounding.
"""

from app.services.solar_assessment import calculate_solar_capacity_factor
from app.services.wind_assessment import calculate_capacity_factor as calculate_wind_capacity_factor

OPERATING_HOURS_PER_YEAR = 8760
DEFAULT_SYSTEM_EFFICIENCY = 0.95  # accounts for inverter/transformer/wiring losses
DEFAULT_OPERATIONAL_LOSS_FACTOR = 0.03  # soiling, downtime, degradation


def _apply_loss_factors(raw_kwh: float, system_efficiency: float, operational_loss_factor: float) -> float:
    return round(raw_kwh * system_efficiency * (1 - operational_loss_factor), 2)


def estimate_solar_yield(installed_capacity_kw: float, solar_irradiance: float,
                          solar_prediction_service=None, features: dict = None,
                          system_efficiency: float = DEFAULT_SYSTEM_EFFICIENCY,
                          operational_loss_factor: float = DEFAULT_OPERATIONAL_LOSS_FACTOR) -> dict:
    if solar_prediction_service is not None and features is not None:
        ml_result = solar_prediction_service.predict(features)
        if ml_result.get("error") is None:
            adjusted = _apply_loss_factors(ml_result["prediction_kwh_year"], system_efficiency, operational_loss_factor)
            return {"annual_energy_kwh": adjusted, "source": "ml_model", "capacity_factor_pct": None}

    # Fallback: rule-based
    capacity_factor = calculate_solar_capacity_factor(solar_irradiance)
    raw_kwh = installed_capacity_kw * (capacity_factor / 100) * OPERATING_HOURS_PER_YEAR
    adjusted = _apply_loss_factors(raw_kwh, system_efficiency, operational_loss_factor)
    return {"annual_energy_kwh": adjusted, "source": "rule_based", "capacity_factor_pct": capacity_factor}


def estimate_wind_yield(installed_capacity_kw: float, wind_speed: float,
                         wind_prediction_service=None, features: dict = None,
                         system_efficiency: float = DEFAULT_SYSTEM_EFFICIENCY,
                         operational_loss_factor: float = DEFAULT_OPERATIONAL_LOSS_FACTOR) -> dict:
    if wind_prediction_service is not None and features is not None:
        ml_result = wind_prediction_service.predict(features)
        if ml_result.get("error") is None:
            adjusted = _apply_loss_factors(ml_result["prediction_kwh_year"], system_efficiency, operational_loss_factor)
            return {"annual_energy_kwh": adjusted, "source": "ml_model", "capacity_factor_pct": None}

    capacity_factor = calculate_wind_capacity_factor(wind_speed)
    raw_kwh = installed_capacity_kw * (capacity_factor / 100) * OPERATING_HOURS_PER_YEAR
    adjusted = _apply_loss_factors(raw_kwh, system_efficiency, operational_loss_factor)
    return {"annual_energy_kwh": adjusted, "source": "rule_based", "capacity_factor_pct": capacity_factor}


def estimate_hybrid_yield(installed_capacity_kw: float, solar_irradiance: float, wind_speed: float,
                           solar_prediction_service=None, wind_prediction_service=None,
                           features: dict = None, hybrid_split: float = 0.5,
                           system_efficiency: float = DEFAULT_SYSTEM_EFFICIENCY,
                           operational_loss_factor: float = DEFAULT_OPERATIONAL_LOSS_FACTOR) -> dict:
    solar_capacity = installed_capacity_kw * hybrid_split
    wind_capacity = installed_capacity_kw * (1 - hybrid_split)

    solar_result = estimate_solar_yield(solar_capacity, solar_irradiance, solar_prediction_service, features,
                                         system_efficiency, operational_loss_factor)
    wind_result = estimate_wind_yield(wind_capacity, wind_speed, wind_prediction_service, features,
                                       system_efficiency, operational_loss_factor)

    return {
        "solar_annual_energy_kwh": solar_result["annual_energy_kwh"],
        "wind_annual_energy_kwh": wind_result["annual_energy_kwh"],
        "total_annual_energy_kwh": round(solar_result["annual_energy_kwh"] + wind_result["annual_energy_kwh"], 2),
        "solar_source": solar_result["source"],
        "wind_source": wind_result["source"],
    }