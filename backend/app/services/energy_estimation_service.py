from app.services.energy_calculator import EnergyCalculator


class EnergyEstimationService:
    """
    Estimates annual energy generation
    based on deployment recommendation.
    """

    def __init__(self):
        self.calculator = EnergyCalculator()

    def estimate_from_features(
        self,
        feature_vector: dict,
    ):
        """
        Estimate annual energy generation
        directly from a feature vector.
        """

        deployment = feature_vector["deployment"]

        return self.estimate_energy(
            deployment_type=deployment,
            installed_capacity=feature_vector["installed_capacity"],
            solar_capacity_factor=feature_vector["solar_capacity_factor"],
            wind_capacity_factor=feature_vector["wind_capacity_factor"],
        )





    def estimate_energy(
        self,
        deployment_type: str,
        installed_capacity: float,
        solar_capacity_factor: float,
        wind_capacity_factor: float,
    ):
        """
        deployment_type:
            Solar
            Wind
            Hybrid
        """

        annual_solar_energy = 0.0
        annual_wind_energy = 0.0

        deployment_type = deployment_type.lower()

        if deployment_type == "solar":

            annual_solar_energy = self.calculator.calculate_solar_energy(
                installed_capacity,
                solar_capacity_factor,
            )

        elif deployment_type == "wind":

            annual_wind_energy = self.calculator.calculate_wind_energy(
                installed_capacity,
                wind_capacity_factor,
            )

        elif deployment_type == "hybrid":

            annual_solar_energy = self.calculator.calculate_solar_energy(
                installed_capacity,
                solar_capacity_factor,
            )

            annual_wind_energy = self.calculator.calculate_wind_energy(
                installed_capacity,
                wind_capacity_factor,
            )

        else:
            raise ValueError(
                "Deployment type must be Solar, Wind, or Hybrid."
            )

        total_energy = (
            annual_solar_energy +
            annual_wind_energy
        )

        return {
            "deployment_type": deployment_type.title(),
            "installed_capacity_kw": installed_capacity,
            "annual_solar_energy_kwh": annual_solar_energy,
            "annual_wind_energy_kwh": annual_wind_energy,
            "total_annual_energy_kwh": total_energy,
        }