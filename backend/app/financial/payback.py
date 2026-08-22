"""
Payback period calculation, with explicit handling for the edge
cases the task specifically calls out (zero/negative revenue).
"""

def calculate_payback_period(total_project_cost: float, annual_revenue: float) -> float | None:
    """
    Returns years to break even, or None if payback is impossible
    (annual_revenue is zero or negative — the project never recovers cost).
    """
    if total_project_cost is None or annual_revenue is None:
        return None
    if annual_revenue <= 0:
        return None
    return round(total_project_cost / annual_revenue, 2)