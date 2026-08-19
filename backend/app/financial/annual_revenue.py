class AnnualRevenueEstimator:

    def estimate(

        self,

        annual_energy_yield,

        electricity_tariff

    ):

        annual_revenue = (

            annual_energy_yield *

            electricity_tariff

        )

        return round(

            annual_revenue,

            2

        )