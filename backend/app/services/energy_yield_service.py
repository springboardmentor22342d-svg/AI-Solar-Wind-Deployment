class EnergyYieldService:

    HOURS_PER_YEAR = 8760

    def calculate_solar_yield(
        self,
        solar_irradiance,
        installed_capacity=100,
        efficiency=0.85
    ):
        """
        Calculate annual solar energy yield.
        """

        return (
            solar_irradiance
            * installed_capacity
            * efficiency
        )

    def calculate_wind_yield(
        self,
        installed_capacity=100,
        capacity_factor=0,
        efficiency=0.90
    ):
        """
        Calculate annual wind energy yield.
        """

        return (
            installed_capacity
            * capacity_factor
            * self.HOURS_PER_YEAR
            * efficiency
        )

    def calculate_hybrid_yield(
        self,
        solar_energy,
        wind_energy
    ):
        """
        Calculate total hybrid energy yield.
        """

        return solar_energy + wind_energy