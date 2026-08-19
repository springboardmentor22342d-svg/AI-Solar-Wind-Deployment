def test_training_service():
    from app.services.training_service import TrainingService

    service = TrainingService()
    result = service.train()
    assert "metrics" in result
    assert "model_path" in result