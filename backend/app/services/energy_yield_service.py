"""
Energy Yield Service — solar/wind/hybrid annual energy estimation.
Uses trained ML predictions where available, falling back to the
rule-based engineering formula when ML prediction is unavailable.
Also provides a qualitative rating/explanation of the resulting yield.
"""

from app.services.solar_assessment import calculate_solar_capacity_factor
from app.services.wind_assessment import calculate_capacity_factor as calculate_wind_capacity_factor

OPERATING_HOURS_PER_YEAR = 8760
DEFAULT_SYSTEM_EFFICIENCY = 0.95
DEFAULT_OPERATIONAL_LOSS_FACTOR = 0.03


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
            return {
                "annual_energy_kwh": adjusted,
                "source": "ml_model",
                "capacity_factor_pct": None,
                "explanation": ml_result.get("explanation"),
            }

    capacity_factor = calculate_solar_capacity_factor(solar_irradiance)
    raw_kwh = installed_capacity_kw * (capacity_factor / 100) * OPERATING_HOURS_PER_YEAR
    adjusted = _apply_loss_factors(raw_kwh, system_efficiency, operational_loss_factor)
    return {
        "annual_energy_kwh": adjusted,
        "source": "rule_based",
        "capacity_factor_pct": capacity_factor,
        "explanation": f"Estimated using rule-based capacity factor ({capacity_factor}%) due to incomplete ML input features.",
    }


def estimate_wind_yield(installed_capacity_kw: float, wind_speed: float,
                         wind_prediction_service=None, features: dict = None,
                         system_efficiency: float = DEFAULT_SYSTEM_EFFICIENCY,
                         operational_loss_factor: float = DEFAULT_OPERATIONAL_LOSS_FACTOR) -> dict:
    if wind_prediction_service is not None and features is not None:
        ml_result = wind_prediction_service.predict(features)
        if ml_result.get("error") is None:
            adjusted = _apply_loss_factors(ml_result["prediction_kwh_year"], system_efficiency, operational_loss_factor)
            return {
                "annual_energy_kwh": adjusted,
                "source": "ml_model",
                "capacity_factor_pct": None,
                "explanation": ml_result.get("explanation"),
            }

    capacity_factor = calculate_wind_capacity_factor(wind_speed)
    raw_kwh = installed_capacity_kw * (capacity_factor / 100) * OPERATING_HOURS_PER_YEAR
    adjusted = _apply_loss_factors(raw_kwh, system_efficiency, operational_loss_factor)
    return {
        "annual_energy_kwh": adjusted,
        "source": "rule_based",
        "capacity_factor_pct": capacity_factor,
        "explanation": f"Estimated using rule-based capacity factor ({capacity_factor}%) due to incomplete ML input features.",
    }


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
        "solar_explanation": solar_result.get("explanation"),
        "wind_explanation": wind_result.get("explanation"),
    }


def rate_energy_yield(annual_energy_kwh: float, deployment_type: str) -> dict:
    """
    Provides a qualitative rating and plain-language explanation of
    the energy yield, based on typical ranges observed across the
    project's training data (~1M-22M kWh/year for a 5000kW reference
    installation).
    """
    if annual_energy_kwh >= 15_000_000:
        rating = "Excellent"
        explanation = "This site's estimated output is among the strongest observed — typical of prime desert or coastal wind corridors."
    elif annual_energy_kwh >= 9_000_000:
        rating = "Good"
        explanation = "This site shows above-average energy potential, suitable for a productive commercial installation."
    elif annual_energy_kwh >= 4_000_000:
        rating = "Average"
        explanation = "This site shows moderate energy potential — commercially viable but not exceptional."
    else:
        rating = "Below Average"
        explanation = "This site's estimated output is on the lower end — may still be viable depending on financial assumptions, but resource conditions are not ideal."

    return {"rating": rating, "explanation": explanation}