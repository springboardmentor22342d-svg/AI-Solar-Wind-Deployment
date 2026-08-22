"""
Orchestrates the full financial analysis, given only plain numeric
inputs — deliberately has no knowledge of ML models, features, or
coordinates, satisfying the module independence requirement.
"""

from app.financial.revenue import estimate_annual_revenue
from app.financial.project_cost import estimate_project_cost, DEFAULT_COST_PER_MW_SOLAR, DEFAULT_COST_PER_MW_WIND
from app.financial.payback import calculate_payback_period
from app.financial.roi import calculate_roi

DEFAULT_TARIFF_PER_KWH = 3.5  # ₹/kWh, typical Indian commercial solar/wind PPA rate


def run_financial_analysis(annual_energy_yield_kwh: float, installed_capacity_kw: float,
                            deployment_type: str, tariff_per_kwh: float = DEFAULT_TARIFF_PER_KWH,
                            installation_overhead_pct: float = 5.0) -> dict:
    cost_per_mw = DEFAULT_COST_PER_MW_WIND if deployment_type == "Wind" else DEFAULT_COST_PER_MW_SOLAR
    # Hybrid uses solar cost as a simplification — could be refined to
    # a weighted blend if the hybrid capacity split is passed through

    annual_revenue = estimate_annual_revenue(annual_energy_yield_kwh, tariff_per_kwh)
    project_cost = estimate_project_cost(installed_capacity_kw, cost_per_mw, installation_overhead_pct)
    payback_period = calculate_payback_period(project_cost, annual_revenue)
    roi = calculate_roi(project_cost, annual_revenue)

    return {
        "annual_energy_yield_kwh": annual_energy_yield_kwh,
        "annual_revenue_inr": annual_revenue,
        "estimated_project_cost_inr": project_cost,
        "payback_period_years": payback_period,
        "roi_pct": roi,
    }