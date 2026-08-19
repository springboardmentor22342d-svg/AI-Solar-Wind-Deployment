def test_prediction_service():
    from app.services.prediction_service import PredictionService

    service = PredictionService()

    sample_features = [7, 15, 196, 28, 31.2, 62.0, 3.5]
    sample_site = {
        "installed_capacity": 500,
        "capacity_factor": 0.25,
        "system_efficiency": 0.85,
        "operational_losses": 0.05,
        "electricity_tariff": 0.12,
        "cost_per_kw": 1100,
        "installation_percentage": 15,
        "protected_area": False,
        "water_body": False,
        "slope": 4,
        "land_area": 25,
        "environmental_rating": 85,
        "economic_rating": 78,
        "distance_to_grid": 1.8,
        "distance_to_road": 0.45
    }

    result = service.predict(sample_features, sample_site)
    assert "prediction" in result
    assert "energy_yield" in result
    assert "financial" in result