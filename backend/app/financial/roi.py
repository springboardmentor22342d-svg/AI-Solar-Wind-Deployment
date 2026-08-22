"""
Return on Investment calculation, expressed as a percentage,
computed over the project's payback-implied lifetime revenue
(a standard simple-ROI approach, not accounting for time value
of money or discounting).
"""

DEFAULT_PROJECT_LIFETIME_YEARS = 25  # typical solar/wind asset lifetime


def calculate_roi(total_project_cost: float, annual_revenue: float,
                   project_lifetime_years: int = DEFAULT_PROJECT_LIFETIME_YEARS) -> float | None:
    if total_project_cost is None or annual_revenue is None or total_project_cost <= 0:
        return None
    total_lifetime_revenue = annual_revenue * project_lifetime_years
    net_gain = total_lifetime_revenue - total_project_cost
    roi_pct = (net_gain / total_project_cost) * 100
    return round(roi_pct, 2)