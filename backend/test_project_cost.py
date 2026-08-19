from app.financial.project_cost import ProjectCostEstimator

estimator = ProjectCostEstimator()

cost = estimator.estimate(

    installed_capacity=100,

    cost_per_kw=50000,

    installation_percentage=10

)

print(cost)