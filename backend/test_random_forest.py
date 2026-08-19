def test_random_forest():
    from app.forecasting.historical_loader import HistoricalDataLoader
    from app.forecasting.time_feature_extractor import TimeFeatureExtractor
    from app.forecasting.dataset_builder import DatasetBuilder
    from app.ml.random_forest_model import RandomForestModel
    from app.ml.model_evaluator import ModelEvaluator

    loader = HistoricalDataLoader("datasets/nasa_power/solar_history.csv")
    dataset = loader.get_dataset()
    extractor = TimeFeatureExtractor()
    dataset = extractor.transform(dataset)
    builder = DatasetBuilder(dataset)
    X, y = builder.build_dataset()

    trainer = RandomForestModel()
    result = trainer.train(X, y)

    evaluator = ModelEvaluator()
    metrics = evaluator.evaluate(result["y_test"], result["predictions"])
    assert "MAE" in metrics or "R2" in metrics or "RMSE" in metrics