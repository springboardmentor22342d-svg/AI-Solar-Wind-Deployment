class EnergyCalculator:
    """
    Utility class for calculating annual
    renewable energy generation.
    """

    OPERATING_HOURS = 8760

    def calculate_solar_energy(
        self,
        installed_capacity: float,
        capacity_factor: float,
    ):
        """
        Annual Solar Energy (kWh)

        Formula:
        Installed Capacity × Capacity Factor × 8760
        """

        annual_energy = (
            installed_capacity
            * capacity_factor
            * self.OPERATING_HOURS
        )

        return round(
            annual_energy,
            2
        )

    def calculate_wind_energy(
        self,
        installed_capacity: float,
        capacity_factor: float,
    ):
        """
        Annual Wind Energy (kWh)

        Formula:
        Installed Capacity × Capacity Factor × 8760
        """

        annual_energy = (
            installed_capacity
            * capacity_factor
            * self.OPERATING_HOURS
        )

        return round(
            annual_energy,
            2
        )