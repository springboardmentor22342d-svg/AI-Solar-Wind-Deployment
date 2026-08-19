from app.services.energy_estimation_service import EnergyEstimationService

service = EnergyEstimationService()

cases = [

    {
        "deployment_type": "Solar",
        "installed_capacity": 100,
        "solar_capacity_factor": 0.25,
        "wind_capacity_factor": 0.35,
    },

    {
        "deployment_type": "Wind",
        "installed_capacity": 100,
        "solar_capacity_factor": 0.25,
        "wind_capacity_factor": 0.35,
    },

    {
        "deployment_type": "Hybrid",
        "installed_capacity": 100,
        "solar_capacity_factor": 0.25,
        "wind_capacity_factor": 0.35,
    }

]

for case in cases:

    print("=" * 60)

    result = service.estimate_energy(**case)

    for key, value in result.items():
        print(f"{key:30}: {value}")

    print()