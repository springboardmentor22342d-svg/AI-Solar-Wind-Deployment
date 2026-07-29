"""
Converts a numeric suitability score into a human-readable
recommendation category, matching the project's own Suitability
Categories (see project PDF, page 7).
"""

def get_recommendation(score: float) -> str:
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Highly Suitable"
    elif score >= 50:
        return "Moderately Suitable"
    elif score >= 30:
        return "Low Suitability"
    else:
        return "Unsuitable"