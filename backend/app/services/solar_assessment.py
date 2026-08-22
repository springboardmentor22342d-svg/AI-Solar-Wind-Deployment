"""
Solar resource classification and capacity factor estimation —
mirrors wind_assessment.py's structure for solar.
"""

def classify_solar_site(solar_irradiance: float) -> str:
    if solar_irradiance is None:
        return "Unknown"
    if solar_irradiance < 4.0:
        return "Poor"
    elif solar_irradiance < 5.0:
        return "Moderate"
    elif solar_irradiance < 6.0:
        return "Good"
    else:
        return "Excellent"


def calculate_solar_capacity_factor(solar_irradiance: float) -> float:
    """
    Estimates capacity factor (%) from solar irradiance, using typical
    ranges for utility-scale fixed-tilt PV in India. Simplified
    lookup, not a full simulation.
    """
    if solar_irradiance is None:
        return 0.0
    solar_class = classify_solar_site(solar_irradiance)
    return {
        "Poor": 12.0,
        "Moderate": 15.0,
        "Good": 18.0,
        "Excellent": 21.0,
    }.get(solar_class, 0.0)