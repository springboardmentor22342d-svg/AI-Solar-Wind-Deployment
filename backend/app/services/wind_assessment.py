"""
Wind resource classification and capacity factor estimation.
No ML yet — uses established wind-speed range thresholds, matching
standard wind resource assessment practice.
"""

def calculate_wind_class(wind_speed: float) -> str:
    """
    Classifies a site's wind resource based on average wind speed (m/s).
    """
    if wind_speed is None:
        return "Unknown"
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
    Estimates capacity factor (%) from wind speed, using typical
    ranges observed for utility-scale turbines. This is a simplified
    lookup, not a physics simulation — real capacity factor depends
    on the full wind speed distribution over a year, not one average.
    """
    if wind_speed is None:
        return 0.0
    if wind_speed < 3:
        return 5.0
    elif wind_speed < 5:
        return 20.0
    elif wind_speed < 7:
        return 35.0
    elif wind_speed < 9:
        return 45.0
    else:
        return 50.0


def classify_wind_site(wind_speed: float) -> dict:
    """
    Combines classification and capacity factor into one result.
    """
    return {
        "wind_class": calculate_wind_class(wind_speed),
        "estimated_capacity_factor_pct": calculate_capacity_factor(wind_speed),
    }
