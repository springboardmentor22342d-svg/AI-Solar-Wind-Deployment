from app.financial.annual_revenue import AnnualRevenueEstimator

estimator = AnnualRevenueEstimator()

revenue = estimator.estimate(

    annual_energy_yield=69921.70,

    electricity_tariff=8

)

print(revenue)