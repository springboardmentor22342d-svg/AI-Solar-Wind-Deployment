class SolarYieldEstimator:

    def estimate(
        self,
        solar_irradiance,
        installed_capacity,
        capacity_factor,
        system_efficiency,
        operational_losses
    ):

        annual_energy = (

            solar_irradiance

            * installed_capacity

            * 365

            * capacity_factor

            * system_efficiency

            * (1 - operational_losses)

        )

        return round(annual_energy, 2)