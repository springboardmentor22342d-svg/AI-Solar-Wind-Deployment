from app.energy.solar_yield import SolarYieldEstimator
from app.energy.wind_yield import WindYieldEstimator
from app.energy.hybrid_yield import HybridYieldEstimator


class EnergyYieldService:

    def __init__(self):

        self.solar = SolarYieldEstimator()

        self.wind = WindYieldEstimator()

        self.hybrid = HybridYieldEstimator()

    def estimate(

        self,

        solar_irradiance,

        wind_speed,

        installed_capacity,

        capacity_factor,

        system_efficiency,

        operational_losses

    ):

        solar_energy = self.solar.estimate(

            solar_irradiance,

            installed_capacity,

            capacity_factor,

            system_efficiency,

            operational_losses

        )

        wind_energy = self.wind.estimate(

            wind_speed,

            installed_capacity,

            capacity_factor,

            system_efficiency,

            operational_losses

        )

        hybrid_energy = self.hybrid.estimate(

            solar_energy,

            wind_energy

        )

        return {

            "solar_energy": solar_energy,

            "wind_energy": wind_energy,

            "hybrid_energy": hybrid_energy

        }