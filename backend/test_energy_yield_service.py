from app.energy.energy_yield_service import EnergyYieldService

service = EnergyYieldService()

result = service.estimate(

    solar_irradiance=5.5,

    wind_speed=6.5,

    installed_capacity=100,

    capacity_factor=0.25,

    system_efficiency=0.92,

    operational_losses=0.08

)

print(result)