def test_deployment_plan_service():
    from app.services.deployment_plan_service import DeploymentPlanService

    service = DeploymentPlanService()

    sites = [
        {"name": "Site A", "deployment_type": "Hybrid", "solar": 0.28, "wind": 0.18, "land": 25, "score": 92},
        {"name": "Site B", "deployment_type": "Wind", "solar": 0.18, "wind": 0.42, "land": 15, "score": 68},
        {"name": "Site C", "deployment_type": "Solar", "solar": 0.30, "wind": 0.36, "land": 8, "score": 40}
    ]

    for site in sites:
        result = service.generate_plan(
            deployment_type=site["deployment_type"],
            solar_capacity_factor=site["solar"],
            wind_capacity_factor=site["wind"],
            land_area=site["land"],
            resource_score=site["score"],
        )
        assert "recommended_technology" in result
        assert "recommended_capacity_kw" in result