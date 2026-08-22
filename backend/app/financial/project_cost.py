"""
Total project cost estimation, based on configurable per-MW cost
assumptions — these are industry-typical reference values, not
site-specific real quotes (no dataset provides actual installation
pricing).
"""

DEFAULT_COST_PER_MW_SOLAR = 35_000_000    # ₹3.5 crore/MW, typical Indian utility-scale solar
DEFAULT_COST_PER_MW_WIND = 60_000_000     # ₹6 crore/MW, typical Indian utility-scale wind
DEFAULT_INSTALLATION_OVERHEAD_PCT = 5.0   # site prep, grid connection, contingency


def estimate_project_cost(installed_capacity_kw: float, cost_per_mw: float,
                           installation_overhead_pct: float = DEFAULT_INSTALLATION_OVERHEAD_PCT) -> float:
    if installed_capacity_kw is None or cost_per_mw is None:
        return 0.0
    installed_capacity_mw = installed_capacity_kw / 1000
    base_cost = installed_capacity_mw * cost_per_mw
    total_cost = base_cost * (1 + installation_overhead_pct / 100)
    return round(total_cost, 2)