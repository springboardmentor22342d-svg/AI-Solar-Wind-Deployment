class ProjectCostEstimator:

    def estimate(

        self,

        installed_capacity,

        cost_per_kw,

        installation_percentage=0

    ):

        base_cost = (

            installed_capacity *

            cost_per_kw

        )

        installation_cost = (

            base_cost *

            installation_percentage /

            100

        )

        total_cost = (

            base_cost +

            installation_cost

        )

        return round(

            total_cost,

            2

        )