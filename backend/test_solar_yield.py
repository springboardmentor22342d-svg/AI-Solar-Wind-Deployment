from app.energy.solar_yield import SolarYieldEstimator

estimator = SolarYieldEstimator()

energy = estimator.estimate(

    solar_irradiance=5.5,

    installed_capacity=200,

    capacity_factor=0.25,

    system_efficiency=0.92,

    operational_losses=0.08

)

print(energy)