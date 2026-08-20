"""
app/services/wind_assessment.py – Wind Resource Assessment Service.

Provides reusable, rule-based engineering functions for wind resource
evaluation.
"""

from __future__ import annotations

import logging
from typing import Literal

logger = logging.getLogger(__name__)

WindClassification = Literal["Poor", "Moderate", "Good", "Excellent"]


# These constants are the single source of truth for thresholds. Changing them
# here automatically updates all downstream logic.
_POOR_MAX: float = 3.0        # m/s  – below this → Poor
_MODERATE_MAX: float = 5.0    # m/s  – [3, 5)    → Moderate
_GOOD_MAX: float = 7.0        # m/s  – [5, 7)    → Good
# ≥ 7.0 m/s                            → Excellent


# Engineering-based rule table derived from typical onshore turbine performance
# curves (Vestas V90, Siemens SWT-2.3, GE 1.85-82.5).
# Each entry: (min_speed_inclusive, max_speed_exclusive, capacity_factor_pct)
_CF_TABLE: list[tuple[float, float, float]] = [
    (0.0,  3.0,   5.0),   # Below cut-in – very minimal or no generation
    (3.0,  4.0,  15.0),   # Near cut-in  – turbine starts generating
    (4.0,  5.0,  22.0),   # Low-moderate – some economic potential
    (5.0,  6.0,  30.0),   # Moderate     – approaching commercial viability
    (6.0,  7.0,  38.0),   # Good         – commercially viable in many markets
    (7.0,  8.0,  45.0),   # Very good    – strong resource, good ROI
    (8.0,  9.0,  52.0),   # Excellent    – premium wind resource
    (9.0,  float("inf"), 58.0),  # Exceptional – offshore-class resource onshore
]



def calculate_wind_class(wind_speed: float) -> int:
    """
    Map a mean annual wind speed to a simplified NREL-inspired wind class (1–4).

    The simplified 4-class scale used here aligns with the qualitative
    classification returned by ``classify_wind_site()`` and is suitable for
    early-stage feasibility screening. For detailed turbine selection,
    use the full NREL 7-class scheme with Weibull parameters.

    Mapping:
        Class 1 → Poor      (< 3 m/s)
        Class 2 → Moderate  (3 – 5 m/s)
        Class 3 → Good      (5 – 7 m/s)
        Class 4 → Excellent (> 7 m/s)

    Args:
        wind_speed (float):
            Mean annual wind speed at hub height in metres per second (m/s).
            Typically sourced from Global Wind Atlas at 50 m or 100 m AGL.

    Returns:
        int: Wind class integer in the range [1, 4].

    Raises:
        TypeError:  If ``wind_speed`` is not a numeric type.
        ValueError: If ``wind_speed`` is negative.

    Examples:
        >>> calculate_wind_class(2.5)
        1
        >>> calculate_wind_class(4.0)
        2
        >>> calculate_wind_class(6.5)
        3
        >>> calculate_wind_class(8.0)
        4
    """
    _validate_wind_speed(wind_speed)

    if wind_speed < _POOR_MAX:
        return 1
    if wind_speed < _MODERATE_MAX:
        return 2
    if wind_speed < _GOOD_MAX:
        return 3
    return 4


def calculate_capacity_factor(wind_speed: float) -> float:
    """
    Estimate the annual capacity factor (%) for a wind turbine at the given
    mean annual wind speed using an engineering rule table.

    This is a *rule-based approximation* intended for early feasibility
    screening. It must NOT be used as a substitute for full bankable energy
    assessments (which require long-term wind time-series, Weibull fitting,
    wake modelling, and site-specific loss analysis).

    Methodology / Assumptions:
        - Reference turbine: modern onshore IEC Class II, 100 m hub height,
          2 MW rated power (e.g. Vestas V90-2.0 performance curve).
        - Cut-in speed: 3 m/s | Rated speed: ~13 m/s | Cut-out speed: 25 m/s.
        - Annual availability: 97 %.
        - Combined losses (wake, electrical, blade): 10 %.
        - Input wind speed represents mean annual value at hub height.
        - Values derived from typical power curve integration over a
          Rayleigh distribution (k=2) at each mid-band wind speed.

    Args:
        wind_speed (float):
            Mean annual wind speed at hub height in metres per second (m/s).

    Returns:
        float: Estimated annual capacity factor as a percentage (0–100).

    Raises:
        TypeError:  If ``wind_speed`` is not a numeric type.
        ValueError: If ``wind_speed`` is negative.

    Examples:
        >>> calculate_capacity_factor(2.0)
        5.0
        >>> calculate_capacity_factor(4.5)
        22.0
        >>> calculate_capacity_factor(6.5)
        38.0
        >>> calculate_capacity_factor(9.5)
        58.0
    """
    _validate_wind_speed(wind_speed)

    for min_spd, max_spd, cf_pct in _CF_TABLE:
        if min_spd <= wind_speed < max_spd:
            logger.debug(
                "capacity_factor: wind_speed=%.2f → cf=%.1f%%", wind_speed, cf_pct
            )
            return cf_pct

    # Fallback – should never be reached given the open-ended last bucket
    logger.warning("capacity_factor: no bucket matched for wind_speed=%.2f", wind_speed)
    return 5.0


def classify_wind_site(wind_speed: float) -> WindClassification:
    """
    Return a human-readable wind site classification based on mean annual
    wind speed.

    Classification table:
        < 3 m/s   → "Poor"
        3–5 m/s   → "Moderate"
        5–7 m/s   → "Good"
        > 7 m/s   → "Excellent"

    This classification is the primary input consumed by the
    ``DeploymentStrategy`` service when comparing wind potential against
    solar potential to recommend the optimal deployment technology.

    Args:
        wind_speed (float):
            Mean annual wind speed at hub height in metres per second (m/s).

    Returns:
        str: One of "Poor", "Moderate", "Good", or "Excellent".

    Raises:
        TypeError:  If ``wind_speed`` is not a numeric type.
        ValueError: If ``wind_speed`` is negative.

    Examples:
        >>> classify_wind_site(1.5)
        'Poor'
        >>> classify_wind_site(3.0)
        'Moderate'
        >>> classify_wind_site(5.0)
        'Good'
        >>> classify_wind_site(7.0)
        'Excellent'
        >>> classify_wind_site(10.0)
        'Excellent'
    """
    _validate_wind_speed(wind_speed)

    if wind_speed < _POOR_MAX:
        return "Poor"
    if wind_speed < _MODERATE_MAX:
        return "Moderate"
    if wind_speed < _GOOD_MAX:
        return "Good"
    return "Excellent"


def get_wind_assessment_summary(wind_speed: float) -> dict:
    """
    Convenience wrapper that calls all three assessment functions and returns
    a consolidated dict. Useful for API responses and report generation.

    Args:
        wind_speed (float): Mean annual wind speed at hub height (m/s).

    Returns:
        dict: Keys ``wind_class`` (int), ``capacity_factor`` (float),
              ``classification`` (str), ``wind_speed_ms`` (float).

    Raises:
        TypeError:  If ``wind_speed`` is not a numeric type.
        ValueError: If ``wind_speed`` is negative.

    Example:
        >>> get_wind_assessment_summary(6.5)
        {
            'wind_speed_ms': 6.5,
            'wind_class': 3,
            'classification': 'Good',
            'capacity_factor': 38.0
        }
    """
    _validate_wind_speed(wind_speed)

    return {
        "wind_speed_ms": wind_speed,
        "wind_class": calculate_wind_class(wind_speed),
        "classification": classify_wind_site(wind_speed),
        "capacity_factor": calculate_capacity_factor(wind_speed),
    }



def _validate_wind_speed(wind_speed: float) -> None:
    """
    Validate that ``wind_speed`` is a non-negative real number.

    Args:
        wind_speed: Value to validate.

    Raises:
        TypeError:  If the value is not int or float.
        ValueError: If the value is negative.
    """
    if not isinstance(wind_speed, (int, float)):
        raise TypeError(
            f"wind_speed must be a numeric value (int or float), "
            f"got {type(wind_speed).__name__!r}."
        )
    if wind_speed < 0:
        raise ValueError(
            f"wind_speed must be non-negative, got {wind_speed}."
        )
