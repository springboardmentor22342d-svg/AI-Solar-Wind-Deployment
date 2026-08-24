
class FinancialAnalysisService:

# -----------------------------------------
# Annual Revenue
# -----------------------------------------

    def estimate_annual_revenue(
    self,
    annual_energy_mwh: float,
    electricity_tariff_inr_per_kwh: float
    ) -> dict:


        if annual_energy_mwh < 0:
            raise ValueError(
        "Annual energy cannot be negative."
        )

        if electricity_tariff_inr_per_kwh < 0:
            raise ValueError(
        "Electricity tariff cannot be negative."
        )

# Convert MWh to kWh
        annual_energy_kwh = (
            annual_energy_mwh * 1000
        )

# Calculate annual revenue
        estimated_annual_revenue_inr = (
            annual_energy_kwh
            * electricity_tariff_inr_per_kwh
        )

        return {
            "annual_energy_mwh": round(
            annual_energy_mwh,
            2
        ),
        "annual_energy_kwh": round(
            annual_energy_kwh,
            2
        ),
        "electricity_tariff_inr_per_kwh": (
            electricity_tariff_inr_per_kwh
        ),
        "estimated_annual_revenue_inr": round(
            estimated_annual_revenue_inr,
            2
        )
    }



# -----------------------------------------
# Total Project Cost
# -----------------------------------------

    def estimate_project_cost(
    self,
    installed_capacity_mw: float,
    cost_per_mw_inr: float,
    additional_installation_percentage: float = 0.0
) -> dict:

        if installed_capacity_mw <= 0:
             raise ValueError(
            "Installed capacity must be greater than 0 MW."
        )

        if cost_per_mw_inr < 0:
             raise ValueError(
            "Cost per MW cannot be negative."
        )

        if additional_installation_percentage < 0:
            raise ValueError(
            "Additional installation percentage "
            "cannot be negative."
        )

        base_project_cost_inr = (
        installed_capacity_mw
        * cost_per_mw_inr
        )

        additional_cost_inr = (
        base_project_cost_inr
        * additional_installation_percentage
        / 100
        )

        total_project_cost_inr = (
            base_project_cost_inr
            + additional_cost_inr
        )

        return {
        "installed_capacity_mw": installed_capacity_mw,
        "cost_per_mw_inr": cost_per_mw_inr,
        "additional_installation_percentage": (
            additional_installation_percentage
        ),
        "base_project_cost_inr": round(
            base_project_cost_inr, 2
        ),
        "additional_cost_inr": round(
            additional_cost_inr, 2
        ),
        "estimated_total_project_cost_inr": round(
            total_project_cost_inr, 2
        )
    }

# -----------------------------------------
# Payback Period
# -----------------------------------------

    def calculate_payback_period(
    self,
    total_project_cost_inr: float,
    annual_revenue_inr: float
    ) -> dict:

        if total_project_cost_inr < 0:
             raise ValueError(
            "Total project cost cannot be negative."
        )

        if annual_revenue_inr < 0:
             raise ValueError(
            "Annual revenue cannot be negative."
        )

    # Zero project cost = immediate recovery
        if total_project_cost_inr == 0:
            return {
            "total_project_cost_inr": total_project_cost_inr,
            "annual_revenue_inr": annual_revenue_inr,
            "payback_period_years": 0,
            "payback_status": "Recoverable"
        }

    # Positive project cost + zero revenue
    # can never recover the investment.
        if annual_revenue_inr == 0:
            return {
            "total_project_cost_inr": total_project_cost_inr,
            "annual_revenue_inr": annual_revenue_inr,
            "payback_period_years": None,
            "payback_status": "Not Recoverable"
        }

        payback_period_years = (
            total_project_cost_inr
            / annual_revenue_inr
        )

        return {
        "total_project_cost_inr": total_project_cost_inr,
        "annual_revenue_inr": annual_revenue_inr,
        "payback_period_years": round(
            payback_period_years,
            2
        ),
        "payback_status": "Recoverable"
    }

# -----------------------------------------
# ROI
# -----------------------------------------

    def calculate_roi(
    self,
    total_project_cost_inr: float,
    annual_revenue_inr: float
    ) -> dict:

        if total_project_cost_inr <= 0:
            raise ValueError(
            "Total project cost must be greater than 0."
        )

        if annual_revenue_inr < 0:
            raise ValueError(
            "Annual revenue cannot be negative."
        )

        roi_percentage = (
            annual_revenue_inr
            / total_project_cost_inr
        ) * 100

        return {
        "total_project_cost_inr": round(
            total_project_cost_inr, 2
        ),
        "annual_revenue_inr": round(
            annual_revenue_inr, 2
        ),
        "roi_percentage": round(
            roi_percentage, 2
        )
    }
