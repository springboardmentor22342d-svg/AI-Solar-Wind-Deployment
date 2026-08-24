from app.energy.solar import estimate_solar_energy
from app.energy.wind import estimate_wind_energy

class EnergyEstimationService:
    def estimate_energy(self,site_result,deployment_type,installed_capacity):
        solar_energy = 0
        wind_energy = 0
        total_energy = 0
        solar_cf = site_result.get("solar_capacity_factor",0.20)
        wind_cf = site_result.get("wind_capacity_factor",0.35)
        if deployment_type.lower() == "solar":
            solar_energy = estimate_solar_energy(installed_capacity,solar_cf)
        elif deployment_type.lower() == "wind":
            wind_energy = estimate_wind_energy(installed_capacity,wind_cf)
        elif deployment_type.lower() == "hybrid":
            solar_energy = estimate_solar_energy(installed_capacity,solar_cf)
            wind_energy = estimate_wind_energy(installed_capacity,wind_cf)
            total_energy = solar_energy + wind_energy
        return {
            "deployment_type": deployment_type,
            "annual_solar_energy": solar_energy,
            "annual_wind_energy": wind_energy,
            "total_annual_energy": total_energy
        }