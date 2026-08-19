class ROICalculator:

    def calculate(

        self,

        annual_revenue,

        total_project_cost

    ):

        if total_project_cost <= 0:

            return None

        roi = (

            annual_revenue /

            total_project_cost

        ) * 100

        return round(

            roi,

            2

        )