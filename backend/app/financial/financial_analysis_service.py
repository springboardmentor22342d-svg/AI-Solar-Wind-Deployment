from app.financial.annual_revenue import AnnualRevenueEstimator
from app.financial.project_cost import ProjectCostEstimator
from app.financial.payback_period import PaybackPeriodCalculator
from app.financial.roi import ROICalculator


class FinancialAnalysisService:

    def __init__(self):

        self.revenue_estimator = AnnualRevenueEstimator()

        self.project_cost_estimator = ProjectCostEstimator()

        self.payback_calculator = PaybackPeriodCalculator()

        self.roi_calculator = ROICalculator()

    def analyze(

        self,

        annual_energy_yield,

        electricity_tariff,

        installed_capacity,

        cost_per_kw,

        installation_percentage=0

    ):

        annual_revenue = self.revenue_estimator.estimate(

            annual_energy_yield,

            electricity_tariff

        )

        total_project_cost = self.project_cost_estimator.estimate(

            installed_capacity,

            cost_per_kw,

            installation_percentage

        )

        payback_period = self.payback_calculator.calculate(

            total_project_cost,

            annual_revenue

        )

        roi = self.roi_calculator.calculate(

            annual_revenue,

            total_project_cost

        )

        return {

            "annual_revenue": annual_revenue,

            "estimated_project_cost": total_project_cost,

            "payback_period": payback_period,

            "roi": roi

        }