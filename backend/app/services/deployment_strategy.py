"""
app/services/deployment_strategy.py – Hybrid Deployment Recommendation Service.

Recommends the most suitable deployment strategy for a given location.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Literal

from app.services.solar_assessment import classify_solar_site
from app.services.wind_assessment import classify_wind_site

logger = logging.getLogger(__name__)

ResourceQuality = Literal["Poor", "Moderate", "Good", "Excellent"]
DeploymentType = Literal["Solar", "Wind", "Hybrid", "Not Recommended"]



@dataclass(frozen=True)
class _Rule:
    """
    Represents a single decision rule in the recommendation table.

    Attributes:
        solar_class:    Qualitative solar resource classification.
        wind_class:     Qualitative wind resource classification.
        deployment:     The recommended deployment strategy.
        confidence:     Base confidence score for this rule (0–100).
        reason:         Human-readable explanation for the recommendation.
    """
    solar_class: ResourceQuality
    wind_class: ResourceQuality
    deployment: DeploymentType
    confidence: int
    reason: str


# Rules are evaluated top-to-bottom; the FIRST matching rule wins.
# To add a new rule: append a ``_Rule(...)`` entry anywhere in this list.
# Ordering: most specific / highest-confidence rules should come first.
_RULES: list[_Rule] = [
    _Rule(
        solar_class="Excellent",
        wind_class="Excellent",
        deployment="Hybrid",
        confidence=95,
        reason="High solar irradiance and consistently strong wind resource.",
    ),
    _Rule(
        solar_class="Excellent",
        wind_class="Good",
        deployment="Hybrid",
        confidence=88,
        reason="Excellent solar potential complemented by a good wind resource.",
    ),
    _Rule(
        solar_class="Excellent",
        wind_class="Moderate",
        deployment="Solar",
        confidence=85,
        reason="Excellent solar potential but moderate wind resource.",
    ),
    _Rule(
        solar_class="Excellent",
        wind_class="Poor",
        deployment="Solar",
        confidence=90,
        reason="Excellent solar potential but weak wind resource.",
    ),
    _Rule(
        solar_class="Good",
        wind_class="Excellent",
        deployment="Hybrid",
        confidence=88,
        reason="Strong wind resource complemented by a good solar potential.",
    ),
    _Rule(
        solar_class="Good",
        wind_class="Good",
        deployment="Hybrid",
        confidence=83,
        reason="Good renewable potential from both solar and wind resources.",
    ),
    _Rule(
        solar_class="Good",
        wind_class="Moderate",
        deployment="Solar",
        confidence=75,
        reason="Good solar irradiance with moderate wind speed favours solar deployment.",
    ),
    _Rule(
        solar_class="Good",
        wind_class="Poor",
        deployment="Solar",
        confidence=78,
        reason="Good solar irradiance with limited wind resource favours solar deployment.",
    ),
    _Rule(
        solar_class="Moderate",
        wind_class="Excellent",
        deployment="Wind",
        confidence=88,
        reason="Strong wind resource with below-average solar irradiance.",
    ),
    _Rule(
        solar_class="Moderate",
        wind_class="Good",
        deployment="Wind",
        confidence=75,
        reason="Good wind resource with moderate solar irradiance favours wind deployment.",
    ),
    _Rule(
        solar_class="Moderate",
        wind_class="Moderate",
        deployment="Solar",
        confidence=55,
        reason="Moderate renewable potential from both resources; solar is the marginal preference.",
    ),
    _Rule(
        solar_class="Moderate",
        wind_class="Poor",
        deployment="Solar",
        confidence=50,
        reason="Moderate solar potential in a low-wind zone; solar is the marginal preference.",
    ),
    _Rule(
        solar_class="Poor",
        wind_class="Excellent",
        deployment="Wind",
        confidence=90,
        reason="Excellent wind resource with insufficient solar irradiance.",
    ),
    _Rule(
        solar_class="Poor",
        wind_class="Good",
        deployment="Wind",
        confidence=78,
        reason="Strong wind resource with poor solar potential.",
    ),
    _Rule(
        solar_class="Poor",
        wind_class="Moderate",
        deployment="Wind",
        confidence=55,
        reason="Moderate wind resource with poor solar irradiance; wind is the marginal preference.",
    ),
    _Rule(
        solar_class="Poor",
        wind_class="Poor",
        deployment="Not Recommended",
        confidence=20,
        reason="Both solar and wind resources are insufficient for cost-effective deployment.",
    ),
]



def recommend_deployment(
    solar_irradiance: float,
    wind_speed: float,
) -> dict:
    """
    Generate a full deployment recommendation for a given location.

    This is the primary entry point for the Deployment Strategy Service.
    It orchestrates calls to ``generate_reason()``, ``confidence_score()``,
    and the internal rule engine to produce the final response dict.

    Args:
        solar_irradiance (float):
            Mean annual Global Horizontal Irradiance (GHI) in kWh/m²/day,
            as returned by the NASA POWER API.
        wind_speed (float):
            Mean annual wind speed at hub height in metres per second (m/s),
            typically from the Global Wind Atlas at 50 m or 100 m AGL.

    Returns:
        dict: Deployment recommendation with the following keys:

            - ``deployment``   (str):  Recommended strategy: "Solar", "Wind",
                                       "Hybrid", or "Not Recommended".
            - ``confidence``   (int):  Confidence score in the range [10, 99].
            - ``reason``       (str):  Human-readable explanation.
            - ``solar_class``  (str):  Derived solar classification.
            - ``wind_class``   (str):  Derived wind classification.

    Raises:
        TypeError:  If either input is not numeric.
        ValueError: If either input is negative.

    Examples:
        >>> recommend_deployment(6.0, 8.0)
        {
            'deployment': 'Hybrid',
            'confidence': 95,
            'reason': 'High solar irradiance and consistently strong wind resource.',
            'solar_class': 'Excellent',
            'wind_class': 'Excellent'
        }

        >>> recommend_deployment(6.0, 2.0)
        {
            'deployment': 'Solar',
            'confidence': 90,
            'reason': 'Excellent solar potential but weak wind resource.',
            'solar_class': 'Excellent',
            'wind_class': 'Poor'
        }
    """
    solar_class: ResourceQuality = classify_solar_site(solar_irradiance)
    wind_class: ResourceQuality = classify_wind_site(wind_speed)

    rule = _lookup_rule(solar_class, wind_class)

    result = {
        "deployment": rule.deployment,
        "confidence": rule.confidence,
        "reason": rule.reason,
        "solar_class": solar_class,
        "wind_class": wind_class,
    }

    logger.info(
        "recommend_deployment: solar=%.2f (%s) wind=%.2f (%s) → %s (confidence=%d)",
        solar_irradiance,
        solar_class,
        wind_speed,
        wind_class,
        rule.deployment,
        rule.confidence,
    )

    return result


def generate_reason(solar_class: ResourceQuality, wind_class: ResourceQuality) -> str:
    """
    Return the human-readable reason string for a given solar/wind class pair.

    Can be called independently when classifications are already known,
    avoiding the need to re-run ``classify_solar_site()`` / ``classify_wind_site()``.

    Args:
        solar_class (str): Solar resource quality – one of
            "Poor", "Moderate", "Good", "Excellent".
        wind_class (str): Wind resource quality – one of
            "Poor", "Moderate", "Good", "Excellent".

    Returns:
        str: Human-readable deployment reason.

    Raises:
        ValueError: If ``solar_class`` or ``wind_class`` is not a recognised value.

    Examples:
        >>> generate_reason("Excellent", "Poor")
        'Excellent solar potential but weak wind resource.'
        >>> generate_reason("Poor", "Excellent")
        'Excellent wind resource with insufficient solar irradiance.'
    """
    _validate_classification(solar_class, "solar_class")
    _validate_classification(wind_class, "wind_class")

    rule = _lookup_rule(solar_class, wind_class)
    return rule.reason


def confidence_score(solar_class: ResourceQuality, wind_class: ResourceQuality) -> int:
    """
    Calculate the rule-based confidence score for a solar/wind class pair.

    The score reflects how strongly the available resource data supports the
    recommendation. It is derived from the rule table and capped to [10, 99].

    Scoring rationale:
        - Both Excellent → ~95  (very strong evidence for Hybrid)
        - One Excellent, one Poor → ~88-90  (clear single-tech preference)
        - Both Moderate or mixed Moderate/Poor → 50–75  (weaker signal)
        - Both Poor → 20  (insufficient resource for any deployment)

    Args:
        solar_class (str): Solar resource quality classification.
        wind_class (str): Wind resource quality classification.

    Returns:
        int: Confidence score in the range [10, 99].

    Raises:
        ValueError: If ``solar_class`` or ``wind_class`` is not a recognised value.

    Examples:
        >>> confidence_score("Excellent", "Excellent")
        95
        >>> confidence_score("Poor", "Poor")
        20
        >>> confidence_score("Good", "Good")
        83
    """
    _validate_classification(solar_class, "solar_class")
    _validate_classification(wind_class, "wind_class")

    rule = _lookup_rule(solar_class, wind_class)
    # Clamp to [10, 99] to avoid implying absolute certainty or impossibility
    return max(10, min(99, rule.confidence))



def _lookup_rule(solar_class: ResourceQuality, wind_class: ResourceQuality) -> _Rule:
    """
    Find the first matching rule in the rule table.

    Args:
        solar_class: Qualitative solar classification.
        wind_class:  Qualitative wind classification.

    Returns:
        _Rule: The first rule whose solar_class and wind_class match.

    Raises:
        RuntimeError: If no matching rule is found (should never happen with a
            complete rule table – indicates a programming error).
    """
    for rule in _RULES:
        if rule.solar_class == solar_class and rule.wind_class == wind_class:
            return rule

    # Safety net – complete rule tables should always match
    raise RuntimeError(
        f"No deployment rule found for solar_class={solar_class!r}, "
        f"wind_class={wind_class!r}. Please extend the _RULES table."
    )


_VALID_CLASSIFICATIONS: frozenset[str] = frozenset(
    {"Poor", "Moderate", "Good", "Excellent"}
)


def _validate_classification(value: str, field_name: str) -> None:
    """
    Validate that a classification string is one of the four accepted values.

    Args:
        value:      The classification string to validate.
        field_name: Name of the field (used in error messages).

    Raises:
        TypeError:  If ``value`` is not a string.
        ValueError: If ``value`` is not a recognised classification.
    """
    if not isinstance(value, str):
        raise TypeError(
            f"{field_name} must be a string, got {type(value).__name__!r}."
        )
    if value not in _VALID_CLASSIFICATIONS:
        raise ValueError(
            f"{field_name} must be one of {sorted(_VALID_CLASSIFICATIONS)}, "
            f"got {value!r}."
        )
