

"""
Wind Assessment Service

This module provides utility functions for:
1. Wind Classification
2. Capacity Factor Estimation
3. Overall Wind Site Assessment
"""


def calculate_wind_class(wind_speed: float) -> str:
    """
    Classify wind speed based on predefined ranges.

    Args:
        wind_speed (float): Wind speed in meters per second (m/s).

    Returns:
        str: Wind classification.
    """

    if wind_speed < 3:
        return "Poor"
    elif 3 <= wind_speed < 5:
        return "Moderate"
    elif 5 <= wind_speed < 7:
"""
Wind Assessment Module

This module evaluates wind resources based on average
wind speed and estimates wind energy potential.
"""

from typing import Dict


def calculate_wind_class(wind_speed: float) -> str:
    """
    Classify wind resource based on average wind speed.
    """
    if wind_speed < 3:
        return "Poor"
    elif wind_speed < 5:
        return "Moderate"
    elif wind_speed < 7:
        return "Good"
    else:
        return "Excellent"


def calculate_capacity_factor(wind_speed: float) -> float:
    """
    Estimate wind turbine capacity factor based on wind speed.

    Capacity Factor Ranges:
    < 3 m/s      -> 0.10 (10%)
    3 - <5 m/s   -> 0.25 (25%)
    5 - <7 m/s   -> 0.40 (40%)
    >= 7 m/s     -> 0.55 (55%)

    Args:
        wind_speed (float): Wind speed in meters per second (m/s).

    Returns:
        float: Estimated capacity factor (0.0 to 1.0).
    """

    if wind_speed < 3:
        return 0.10
    elif wind_speed < 5:
        return 0.25
    elif wind_speed < 7:
        return 0.40
    else:
        return 0.55


def classify_wind_site(wind_speed: float) -> dict:
    """
    Assess a wind site using wind speed.

    Args:
        wind_speed (float): Wind speed in meters per second (m/s).

    Returns:
        dict: Wind assessment results.
    """

    return {
        "wind_speed": wind_speed,
        "wind_class": calculate_wind_class(wind_speed),
        "capacity_factor": calculate_capacity_factor(wind_speed)
def calculate_capacity_factor(wind_speed: float) -> int:
    """
    Estimate wind turbine capacity factor (%)
    using wind speed ranges.
    """
    if wind_speed < 3:
        return 0
    elif wind_speed < 5:
        return 20
    elif wind_speed < 7:
        return 35
    else:
        return 50


def classify_wind_site(wind_speed: float) -> Dict:
    """
    Perform complete wind assessment.
    """
    return {
        "wind_speed": wind_speed,
        "wind_class": calculate_wind_class(wind_speed),
        "capacity_factor": calculate_capacity_factor(wind_speed),
    }


# ==========================================
# Improved / Extended Wind Assessment Functions
# ==========================================

def calculate_wind_resource_score(wind_speed: float) -> float:
    """
    Calculate a wind resource score from 0 to 100.
    """
    return round(max(0.0, min(100.0, (wind_speed / 12.0) * 100)), 2)


def calculate_annual_energy_production(capacity_factor: float) -> float:
    """
    Estimate the Annual Energy Production in kWh per kW of installed capacity.
    """
    return round(8760.0 * (capacity_factor / 100.0), 2)


def calculate_wind_suitability(wind_speed: float) -> Dict:
    """
    Score and classify wind suitability based on average wind speed.
    """
    score = calculate_wind_resource_score(wind_speed)
    if score >= 80:
        category = "Excellent"
    elif score >= 65:
        category = "Highly Suitable"
    elif score >= 50:
        category = "Moderately Suitable"
    elif score >= 35:
        category = "Low Suitability"
    else:
        category = "Unsuitable"

    return {
        "score": score,
        "category": category
    }


def assess_wind(wind_speed: float) -> Dict:
    """
    Perform improved complete wind assessment.
    """
    cf = float(calculate_capacity_factor(wind_speed))
    suit = calculate_wind_suitability(wind_speed)
    return {
        "wind_speed": wind_speed,
        "wind_class": calculate_wind_class(wind_speed),
        "capacity_factor": cf,
        "wind_resource_score": suit["score"],
        "wind_suitability": suit["category"],
        "annual_energy_production": calculate_annual_energy_production(cf)
    }