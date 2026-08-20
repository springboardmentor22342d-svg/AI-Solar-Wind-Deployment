from fastapi import APIRouter

router = APIRouter()

SOLAR_GUIDELINES = [
    {"range": "Below 4.0 kWh/m²/day", "rating": "Poor", "description": "Insufficient sunlight for commercially viable solar generation."},
    {"range": "4.0 – 5.0 kWh/m²/day", "rating": "Moderate", "description": "Workable for solar, but not among the strongest sites."},
    {"range": "5.0 – 6.0 kWh/m²/day", "rating": "Good", "description": "Solid solar resource, typical of productive commercial installations."},
    {"range": "Above 6.0 kWh/m²/day", "rating": "Excellent", "description": "Among the strongest solar resource available — typical of desert regions like Rajasthan."},
]

WIND_GUIDELINES = [
    {"range": "Below 3 m/s", "rating": "Poor", "description": "Below typical turbine cut-in speed — little to no usable wind energy."},
    {"range": "3 – 5 m/s", "rating": "Moderate", "description": "Workable for wind, but turbines will run well below rated capacity."},
    {"range": "5 – 7 m/s", "rating": "Good", "description": "Solid wind resource, suitable for productive commercial turbines."},
    {"range": "Above 7 m/s", "rating": "Excellent", "description": "Among the strongest wind resource available — typical of coastal corridors and open plains like Tamil Nadu's Muppandal region."},
]

@router.get("/guidelines")
def get_guidelines():
    return {
        "solar_irradiance_guide": SOLAR_GUIDELINES,
        "wind_speed_guide": WIND_GUIDELINES,
        "note": "Ratings reflect typical ranges for utility-scale renewable installations in India, consistent with the thresholds used throughout this platform's analysis.",
    }