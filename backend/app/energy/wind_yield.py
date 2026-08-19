class WindYieldEstimator:

    def estimate(
        self,
        wind_speed,
        installed_capacity,
        capacity_factor,
        system_efficiency,
        operational_losses
    ):

        annual_energy = (

            wind_speed

            * installed_capacity

            * 365

            * capacity_factor

            * system_efficiency

            * (1 - operational_losses)

        )

        return round(annual_energy, 2)