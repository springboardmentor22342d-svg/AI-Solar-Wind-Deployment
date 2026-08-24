from app.energy.solar import estimate_solar_energy
from app.energy.wind import estimate_wind_energy
def estimate_hybrid_energy(installed_capacity,solar_capacity_factor,wind_capacity_factor):
    solar = estimate_solar_energy(installed_capacity,solar_capacity_factor)
    wind = estimate_wind_energy(installed_capacity,wind_capacity_factor)
    return{
        "solar_energy": solar,
        "wind_energy": wind,
        "total_energy": solar + wind
    }