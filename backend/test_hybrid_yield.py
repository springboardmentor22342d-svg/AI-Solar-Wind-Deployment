from app.energy.hybrid_yield import HybridYieldEstimator

estimator = HybridYieldEstimator()

hybrid = estimator.estimate(

    solar_energy=42478.70,

    wind_energy=67260.38

)

print(hybrid)