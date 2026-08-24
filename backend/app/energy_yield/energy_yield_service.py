


class EnergyYieldService:
    """
    Service for estimating annual renewable energy generation.
    """

    HOURS_PER_YEAR = 8760

    # -----------------------------------------
    # Generic Annual Energy
    # -----------------------------------------

    def estimate_annual_energy(
        self,
        installed_capacity_mw: float,
        capacity_factor: float,
        system_efficiency: float = 1.0,
        operational_losses: float = 0.0
    ) -> dict:

        if installed_capacity_mw <= 0:
            raise ValueError(
                "Installed capacity must be greater than 0 MW."
            )

        if not 0 <= capacity_factor <= 1:
            raise ValueError(
                "Capacity factor must be between 0 and 1."
            )

        if not 0 < system_efficiency <= 1:
            raise ValueError(
                "System efficiency must be greater than 0 and at most 1."
            )

        if not 0 <= operational_losses <= 1:
            raise ValueError(
                "Operational losses must be between 0 and 1."
            )

        annual_energy_mwh = (
            installed_capacity_mw
            * self.HOURS_PER_YEAR
            * capacity_factor
            * system_efficiency
            * (1 - operational_losses)
        )

        return {
            "installed_capacity_mw": installed_capacity_mw,
            "capacity_factor": capacity_factor,
            "system_efficiency": system_efficiency,
            "operational_losses": operational_losses,
            "annual_energy_mwh": round(annual_energy_mwh, 2),
            "annual_energy_gwh": round(annual_energy_mwh / 1000, 2)
        }

    # -----------------------------------------
    # Solar Energy
    # -----------------------------------------

    def estimate_solar_energy(
        self,
        installed_capacity_mw: float,
        solar_irradiance: float,
        capacity_factor: float = None,
        system_efficiency: float = 0.90,
        operational_losses: float = 0.10
    ) -> dict:

        if solar_irradiance < 0:
            raise ValueError(
                "Solar irradiance cannot be negative."
            )

        # If capacity factor is not explicitly provided,
        # estimate it from solar irradiance.
        if capacity_factor is None:
            capacity_factor = min(
                max(solar_irradiance / 12.0, 0.0),
                1.0
            )

        result = self.estimate_annual_energy(
            installed_capacity_mw=installed_capacity_mw,
            capacity_factor=capacity_factor,
            system_efficiency=system_efficiency,
            operational_losses=operational_losses
        )

        return {
            "technology": "Solar",
            "solar_irradiance": solar_irradiance,
            **result
        }

    # -----------------------------------------
    # Wind Energy
    # -----------------------------------------

    def estimate_wind_energy(
        self,
        installed_capacity_mw: float,
        wind_speed: float,
        capacity_factor: float = None,
        system_efficiency: float = 0.90,
        operational_losses: float = 0.10
    ) -> dict:

        if wind_speed < 0:
            raise ValueError(
                "Wind speed cannot be negative."
            )

        # If capacity factor is not explicitly provided,
        # estimate it from wind speed.
        if capacity_factor is None:
            capacity_factor = min(
                max((wind_speed / 15.0) ** 3, 0.0),
                1.0
            )

        result = self.estimate_annual_energy(
            installed_capacity_mw=installed_capacity_mw,
            capacity_factor=capacity_factor,
            system_efficiency=system_efficiency,
            operational_losses=operational_losses
        )

        return {
            "technology": "Wind",
            "wind_speed": wind_speed,
            **result
        }

    # -----------------------------------------
    # Hybrid Energy
    # -----------------------------------------

    def estimate_hybrid_energy(
        self,
        solar_capacity_mw: float,
        wind_capacity_mw: float,
        solar_irradiance: float,
        wind_speed: float,
        solar_capacity_factor: float = None,
        wind_capacity_factor: float = None,
        system_efficiency: float = 0.90,
        operational_losses: float = 0.10
    ) -> dict:

        solar = self.estimate_solar_energy(
            installed_capacity_mw=solar_capacity_mw,
            solar_irradiance=solar_irradiance,
            capacity_factor=solar_capacity_factor,
            system_efficiency=system_efficiency,
            operational_losses=operational_losses
        )

        wind = self.estimate_wind_energy(
            installed_capacity_mw=wind_capacity_mw,
            wind_speed=wind_speed,
            capacity_factor=wind_capacity_factor,
            system_efficiency=system_efficiency,
            operational_losses=operational_losses
        )

        total_mwh = (
            solar["annual_energy_mwh"]
            + wind["annual_energy_mwh"]
        )

        return {
            "technology": "Hybrid",
            "solar": solar,
            "wind": wind,
            "total_annual_energy_mwh": round(total_mwh, 2),
            "total_annual_energy_gwh": round(total_mwh / 1000, 2)
        }
