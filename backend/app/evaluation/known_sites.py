"""
Flags proximity to known major renewable installations, to avoid
recommending sites that are effectively already developed.
Curated list, not a live registry (no public real-time API exists
for this in India) — documented limitation.
"""

import math

KNOWN_INSTALLATIONS = [
    {"name": "Bhadla Solar Park", "lat": 27.5397, "lon": 71.9153, "type": "Solar"},
    {"name": "Pavagada Solar Park", "lat": 14.25, "lon": 77.45, "type": "Solar"},
    {"name": "Muppandal Wind Farm", "lat": 8.25, "lon": 77.59, "type": "Wind"},
]

PROXIMITY_THRESHOLD_KM = 10.0


def check_nearby_known_installations(latitude: float, longitude: float) -> dict:
    km_per_deg_lat = 111.0
    km_per_deg_lon = 111.0 * math.cos(math.radians(latitude))
    avg_km_per_deg = (km_per_deg_lat + km_per_deg_lon) / 2

    for site in KNOWN_INSTALLATIONS:
        dist_deg = ((site["lat"] - latitude) ** 2 + (site["lon"] - longitude) ** 2) ** 0.5
        dist_km = dist_deg * avg_km_per_deg
        if dist_km <= PROXIMITY_THRESHOLD_KM:
            return {
                "nearby_installation": True,
                "installation_name": site["name"],
                "installation_type": site["type"],
                "distance_km": round(dist_km, 2),
                "note": f"This location is within {round(dist_km, 1)}km of {site['name']}, an existing {site['type']} installation.",
            }

    return {"nearby_installation": False, "installation_name": None, "installation_type": None, "distance_km": None, "note": None}