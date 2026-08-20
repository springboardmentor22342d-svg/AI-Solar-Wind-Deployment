"""
app/services/solar_assessment.py – Solar Resource Assessment Service.

Provides reusable, rule-based engineering functions for solar resource
evaluation.
"""

from __future__ import annotations

import logging
from typing import Literal

logger = logging.getLogger(__name__)

SolarClassification = Literal["Poor", "Moderate", "Good", "Excellent"]


# Based on ESMAP/World Bank global solar resource classifications
_POOR_MAX: float = 3.5        # kWh/m²/day – below this → Poor
_MODERATE_MAX: float = 4.5    # kWh/m²/day – [3.5, 4.5) → Moderate
_GOOD_MAX: float = 5.5        # kWh/m²/day – [4.5, 5.5) → Good
# ≥ 5.5 kWh/m²/day                          → Excellent


# Engineering-based rule table for fixed-tilt crystalline silicon PV systems.
# Each entry: (min_irradiance_inclusive, max_irradiance_exclusive, capacity_factor_pct)
_CF_TABLE: list[tuple[float, float, float]] = [
    (0.0,  2.0,   5.0),   # Very low irradiance – marginal generation
    (2.0,  3.5,  12.0),   # Low irradiance – below economic threshold
    (3.5,  4.5,  17.0),   # Moderate – approaching commercial viability
    (4.5,  5.5,  20.0),   # Good – commercially viable in most markets
    (5.5,  6.5,  24.0),   # Very good – strong resource, good ROI
    (6.5,  7.5,  27.0),   # Excellent – premium solar resource (desert regions)
    (7.5,  float("inf"), 30.0),  # Exceptional – high-altitude desert / DNI-rich sites
]



def calculate_solar_class(solar_irradiance: float) -> int:
    """
    Map a mean annual GHI value to a simplified solar resource class (1–4).

    Mapping:
        Class 1 → Poor      (< 3.5 kWh/m²/day)
        Class 2 → Moderate  (3.5 – 4.5 kWh/m²/day)
        Class 3 → Good      (4.5 – 5.5 kWh/m²/day)
        Class 4 → Excellent (≥ 5.5 kWh/m²/day)

    Args:
        solar_irradiance (float):
            Mean annual Global Horizontal Irradiance (GHI) in kWh/m²/day,
            as returned by the NASA POWER API.

    Returns:
        int: Solar class integer in the range [1, 4].

    Raises:
        TypeError:  If ``solar_irradiance`` is not a numeric type.
        ValueError: If ``solar_irradiance`` is negative.

    Examples:
        >>> calculate_solar_class(3.0)
        1
        >>> calculate_solar_class(4.0)
        2
        >>> calculate_solar_class(5.0)
        3
        >>> calculate_solar_class(6.0)
        4
    """
    _validate_solar_irradiance(solar_irradiance)

    if solar_irradiance < _POOR_MAX:
        return 1
    if solar_irradiance < _MODERATE_MAX:
        return 2
    if solar_irradiance < _GOOD_MAX:
        return 3
    return 4


def calculate_solar_capacity_factor(solar_irradiance: float) -> float:
    """
    Estimate the annual capacity factor (%) for a fixed-tilt PV system at
    the given mean annual GHI value using an engineering rule table.

    This is a *rule-based approximation* for early feasibility screening.
    For bankable energy assessments, use full PVsyst / SAM simulations with
    hourly irradiance time-series, temperature corrections, and detailed
    loss modelling.

    Methodology / Assumptions:
        - Fixed-tilt monocrystalline silicon system at optimal tilt angle.
        - System performance ratio: 80 % (IEC 61724 compliant).
        - Panel efficiency: 20 % (standard commercial modules).
        - Annual availability: 99 % (no scheduled outages).
        - Input irradiance: mean annual GHI in kWh/m²/day.
        - Capacity factor = (annual generation in kWh) / (peak power × 8760 h).

    Args:
        solar_irradiance (float):
            Mean annual GHI in kWh/m²/day.

    Returns:
        float: Estimated annual capacity factor as a percentage (0–100).

    Raises:
        TypeError:  If ``solar_irradiance`` is not a numeric type.
        ValueError: If ``solar_irradiance`` is negative.

    Examples:
        >>> calculate_solar_capacity_factor(1.5)
        5.0
        >>> calculate_solar_capacity_factor(4.0)
        17.0
        >>> calculate_solar_capacity_factor(5.0)
        20.0
        >>> calculate_solar_capacity_factor(8.0)
        30.0
    """
    _validate_solar_irradiance(solar_irradiance)

    for min_irr, max_irr, cf_pct in _CF_TABLE:
        if min_irr <= solar_irradiance < max_irr:
            logger.debug(
                "solar_capacity_factor: irradiance=%.2f → cf=%.1f%%",
                solar_irradiance,
                cf_pct,
            )
            return cf_pct

    logger.warning(
        "solar_capacity_factor: no bucket matched for irradiance=%.2f",
        solar_irradiance,
    )
    return 5.0


def classify_solar_site(solar_irradiance: float) -> SolarClassification:
    """
    Return a human-readable solar site classification based on mean annual GHI.

    Classification table:
        < 3.5 kWh/m²/day  → "Poor"
        3.5–4.5            → "Moderate"
        4.5–5.5            → "Good"
        ≥ 5.5              → "Excellent"

    This classification is the primary solar input consumed by the
    ``DeploymentStrategy`` service.

    Args:
        solar_irradiance (float):
            Mean annual Global Horizontal Irradiance (GHI) in kWh/m²/day.

    Returns:
        str: One of "Poor", "Moderate", "Good", or "Excellent".

    Raises:
        TypeError:  If ``solar_irradiance`` is not a numeric type.
        ValueError: If ``solar_irradiance`` is negative.

    Examples:
        >>> classify_solar_site(3.0)
        'Poor'
        >>> classify_solar_site(4.0)
        'Moderate'
        >>> classify_solar_site(5.0)
        'Good'
        >>> classify_solar_site(6.0)
        'Excellent'
    """
    _validate_solar_irradiance(solar_irradiance)

    if solar_irradiance < _POOR_MAX:
        return "Poor"
    if solar_irradiance < _MODERATE_MAX:
        return "Moderate"
    if solar_irradiance < _GOOD_MAX:
        return "Good"
    return "Excellent"


def get_solar_assessment_summary(solar_irradiance: float) -> dict:
    """
    Convenience wrapper that calls all three assessment functions and returns
    a consolidated dict. Mirrors ``wind_assessment.get_wind_assessment_summary()``.

    Args:
        solar_irradiance (float): Mean annual GHI in kWh/m²/day.

    Returns:
        dict: Keys ``solar_irradiance_kwh`` (float), ``solar_class`` (int),
              ``classification`` (str), ``capacity_factor`` (float).

    Raises:
        TypeError:  If ``solar_irradiance`` is not a numeric type.
        ValueError: If ``solar_irradiance`` is negative.

    Example:
        >>> get_solar_assessment_summary(5.0)
        {
            'solar_irradiance_kwh': 5.0,
            'solar_class': 3,
            'classification': 'Good',
            'capacity_factor': 20.0
        }
    """
    _validate_solar_irradiance(solar_irradiance)

    return {
        "solar_irradiance_kwh": solar_irradiance,
        "solar_class": calculate_solar_class(solar_irradiance),
        "classification": classify_solar_site(solar_irradiance),
        "capacity_factor": calculate_solar_capacity_factor(solar_irradiance),
    }



def _validate_solar_irradiance(solar_irradiance: float) -> None:
    """
    Validate that ``solar_irradiance`` is a non-negative real number.

    Args:
        solar_irradiance: Value to validate.

    Raises:
        TypeError:  If the value is not int or float.
        ValueError: If the value is negative.
    """
    if not isinstance(solar_irradiance, (int, float)):
        raise TypeError(
            f"solar_irradiance must be a numeric value (int or float), "
            f"got {type(solar_irradiance).__name__!r}."
        )
    if solar_irradiance < 0:
        raise ValueError(
            f"solar_irradiance must be non-negative, got {solar_irradiance}."
        )
