from app.services.energy_estimation_service import EnergyEstimationService

service = EnergyEstimationService()

sample_sites = [

    {
        "site_name": "Solar Farm",
        "deployment_type": "Solar",
        "installed_capacity": 150,
        "solar_capacity_factor": 0.26,
        "wind_capacity_factor": 0.35,
    },

    {
        "site_name": "Wind Farm",
        "deployment_type": "Wind",
        "installed_capacity": 150,
        "solar_capacity_factor": 0.26,
        "wind_capacity_factor": 0.42,
    },

    {
        "site_name": "Hybrid Farm",
        "deployment_type": "Hybrid",
        "installed_capacity": 150,
        "solar_capacity_factor": 0.26,
        "wind_capacity_factor": 0.42,
    }

]

for site in sample_sites:

    print("=" * 70)
    print(f"Site: {site['site_name']}")

    result = service.estimate_energy(
        deployment_type=site["deployment_type"],
        installed_capacity=site["installed_capacity"],
        solar_capacity_factor=site["solar_capacity_factor"],
        wind_capacity_factor=site["wind_capacity_factor"],
    )

    for key, value in result.items():
        print(f"{key:30}: {value}")

    print()