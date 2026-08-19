class PaybackPeriodCalculator:

    def calculate(

        self,

        total_project_cost,

        annual_revenue

    ):

        if annual_revenue <= 0:

            return None

        years = (

            total_project_cost /

            annual_revenue

        )

        return round(

            years,

            2

        )