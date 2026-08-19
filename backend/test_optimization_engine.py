def test_optimization_engine():
    from app.services.deployment_plan_service import DeploymentPlanService

    service = DeploymentPlanService()

    sample_sites = [
        {"site_name": "Solar Valley", "deployment_type": "Solar", "solar_capacity_factor": 0.30, "wind_capacity_factor": 0.18, "land_area": 30, "resource_score": 95},
        {"site_name": "Wind Ridge", "deployment_type": "Wind", "solar_capacity_factor": 0.18, "wind_capacity_factor": 0.42, "land_area": 18, "resource_score": 75},
        {"site_name": "Hybrid Plains", "deployment_type": "Hybrid", "solar_capacity_factor": 0.28, "wind_capacity_factor": 0.36, "land_area": 25, "resource_score": 90}
    ]

    for site in sample_sites:
        result = service.generate_plan(
            deployment_type=site["deployment_type"],
            solar_capacity_factor=site["solar_capacity_factor"],
            wind_capacity_factor=site["wind_capacity_factor"],
            land_area=site["land_area"],
            resource_score=site["resource_score"],
        )
        assert result["recommended_capacity_kw"] > 0