"""
Expansion feasibility — determines whether a site has room to grow
beyond its currently planned capacity.
"""

from app.optimization.constraints import (
    EXPANSION_HEADROOM_RATIO_EXPANDABLE,
    EXPANSION_HEADROOM_RATIO_LIMITED,
    MIN_SPARE_LAND_HECTARES_EXPANDABLE,
    MIN_SPARE_LAND_HECTARES_LIMITED,
)


def analyze_expansion_feasibility(total_land_area_hectares: float, land_area_used_hectares: float) -> str:
    """
    Combines two checks: the RATIO of spare-to-used land, AND the
    ABSOLUTE amount of spare land. Both must clear their thresholds —
    a small site can't be "Expandable" just by matching the same
    ratio as a much larger site with more genuine room to grow.
    """
    if total_land_area_hectares is None or land_area_used_hectares is None or land_area_used_hectares == 0:
        return "Not Expandable"

    spare_land_hectares = total_land_area_hectares - land_area_used_hectares
    headroom_ratio = total_land_area_hectares / land_area_used_hectares

    if headroom_ratio >= EXPANSION_HEADROOM_RATIO_EXPANDABLE and spare_land_hectares >= MIN_SPARE_LAND_HECTARES_EXPANDABLE:
        return "Expandable"
    elif headroom_ratio >= EXPANSION_HEADROOM_RATIO_LIMITED and spare_land_hectares >= MIN_SPARE_LAND_HECTARES_LIMITED:
        return "Limited Expansion"
    else:
        return "Not Expandable"