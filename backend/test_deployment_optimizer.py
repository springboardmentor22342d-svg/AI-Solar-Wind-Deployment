from app.services.deployment_optimizer import DeploymentOptimizer

optimizer = DeploymentOptimizer()

sites = [

    {
        "name": "Site A",
        "solar": 0.28,
        "wind": 0.18,
    },

    {
        "name": "Site B",
        "solar": 0.18,
        "wind": 0.42,
    },

    {
        "name": "Site C",
        "solar": 0.29,
        "wind": 0.38,
    },

]

for site in sites:

    print("=" * 60)

    print(site["name"])

    print(
        optimizer.recommend_deployment(
            site["solar"],
            site["wind"],
        )
    )