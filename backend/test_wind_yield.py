from app.energy.wind_yield import WindYieldEstimator

estimator = WindYieldEstimator()

energy = estimator.estimate(

    wind_speed=3.0,

    installed_capacity=100,

    capacity_factor=0.35,

    system_efficiency=0.90,

    operational_losses=0.10

)

print(energy)