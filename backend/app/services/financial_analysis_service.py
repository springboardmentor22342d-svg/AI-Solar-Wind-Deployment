class FinancialAnalysisService:
    def calaculate_annual_revenue(
            self,
            annual_energy_yield,
            electricity_tariff
    ):
        """
        Annual Revenue (₹)
        """
        return annual_energy_yield * electricity_tariff
    def calculate_project_cost(
            self,
            installed_capacity,
            cost_per_mw,
            installation_percentage=0
    ):
        """
        Total Poject Cost (₹)
        """
        base_cost = installed_capacity * cost_per_mw
        installation_cost = base_cost * installation_percentage/100
        return base_cost + installation_cost
    def calculate_payback_period(
            seld,
            project_cost,
            annual_revenue
    ):
        """
        Payback Period (Years)
        """
        if annual_revenue <= 0:
            return None
        return project_cost / annual_revenue
    def calculate_roi(
            self,
            annual_revenue,
            project_cost
    ):
        """
        Return onInvestment (%)
        """
        if project_cost <= 0:
            return 0
        return ((annual_revenue - project_cost) / project_cost) * 100