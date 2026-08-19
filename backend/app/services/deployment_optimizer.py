class DeploymentOptimizer:
    """
    Determines the optimal deployment
    technology for a site.
    """

    def recommend_deployment(
        self,
        solar_capacity_factor: float,
        wind_capacity_factor: float,
    ):

        if (
            solar_capacity_factor >= 0.25
            and
            wind_capacity_factor >= 0.35
        ):
            recommendation = "Hybrid"

        elif solar_capacity_factor >= wind_capacity_factor:
            recommendation = "Solar"

        else:
            recommendation = "Wind"

        return {
            "recommended_technology": recommendation,
            "solar_capacity_factor": solar_capacity_factor,
            "wind_capacity_factor": wind_capacity_factor,
        }