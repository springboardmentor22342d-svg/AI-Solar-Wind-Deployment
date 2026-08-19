class CapacityPlanner:
    """
    Estimates the recommended installation
    capacity based on available land and
    resource availability.
    """

    LAND_UTILIZATION_FACTOR = 50
    # Assume 50 kW can be installed per acre.

    def recommend_capacity(
        self,
        land_area: float,
        resource_score: float,
    ):
        """
        Parameters:
            land_area      : Acres
            resource_score : 0–100
        """

        base_capacity = (
            land_area *
            self.LAND_UTILIZATION_FACTOR
        )

        utilization = resource_score / 100

        recommended_capacity = (
            base_capacity *
            utilization
        )

        return {
            "land_area_acres": land_area,
            "resource_score": resource_score,
            "recommended_capacity_kw": round(
                recommended_capacity,
                2
            )
        }