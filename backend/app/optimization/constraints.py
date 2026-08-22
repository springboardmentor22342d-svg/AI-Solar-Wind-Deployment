"""
Optimization constraints — configurable limits, not derived from
site data (land area, budget, and grid capacity are project-specific
inputs, not something any dataset can tell us).
"""

# Land use assumptions (hectares needed per MW of installed capacity)
SOLAR_LAND_USE_HA_PER_MW = 2.0    # typical range: 1.5-2.5 ha/MW for fixed-tilt PV
WIND_LAND_USE_HA_PER_MW = 6.0     # accounts for turbine spacing requirements, not just footprint

# Absolute minimum spare land (hectares) required to be genuinely
# "Expandable" — prevents tiny sites from being labeled expandable
# purely because they follow the same 60% utilization ratio as huge sites
MIN_SPARE_LAND_HECTARES_EXPANDABLE = 50.0
MIN_SPARE_LAND_HECTARES_LIMITED = 10.0

# Grid capacity — example default, meant to be overridden per real substation data
DEFAULT_GRID_CAPACITY_LIMIT_MW = 50.0

# Expansion thresholds
EXPANSION_HEADROOM_RATIO_EXPANDABLE = 1.5   # 50%+ unused land beyond current plan
EXPANSION_HEADROOM_RATIO_LIMITED = 1.1      # 10-50% unused land


def check_land_area_constraint(land_area_hectares: float, required_hectares: float) -> bool:
    if land_area_hectares is None or required_hectares is None:
        return False
    return land_area_hectares >= required_hectares


def check_budget_constraint(estimated_cost: float, budget: float) -> bool:
    if estimated_cost is None or budget is None:
        return False
    return estimated_cost <= budget


def check_grid_capacity_constraint(installed_capacity_mw: float,
                                    grid_capacity_limit_mw: float = DEFAULT_GRID_CAPACITY_LIMIT_MW) -> bool:
    if installed_capacity_mw is None:
        return False
    return installed_capacity_mw <= grid_capacity_limit_mw