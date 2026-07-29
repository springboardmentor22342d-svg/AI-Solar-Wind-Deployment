"""
Weighted scoring configuration, aligned with the project's own
suitability scoring model (see project PDF, Weighted Scoring Model):
    Renewable Resource Availability: 35%
    Geographic Suitability:          25%
    Infrastructure Accessibility:    15%
    Environmental Impact:            15%
    Economic Feasibility:            10%

Mapped to available features:
    Resource Availability -> solar_irradiance + wind_speed
    Geographic Suitability -> slope
    Infrastructure Accessibility -> distance_to_nearest_settlement_km
        (proxy for combined grid + road distance — no separate
        grid/road distance data is currently available)
    Environmental Impact -> forest_pct, culturable_wasteland_pct
    Economic Feasibility -> distance_to_nearest_settlement_km
        (proxy — closer to settlements generally implies lower
        connection/labor cost)
"""

WEIGHT_RESOURCE_AVAILABILITY = 0.35
WEIGHT_GEOGRAPHIC_SUITABILITY = 0.25
WEIGHT_INFRASTRUCTURE = 0.15
WEIGHT_ENVIRONMENTAL_IMPACT = 0.15
WEIGHT_ECONOMIC_FEASIBILITY = 0.10

# Sub-weights within Resource Availability (solar vs wind)
SOLAR_SUB_WEIGHT = 0.5
WIND_SUB_WEIGHT = 0.5