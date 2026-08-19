from app.forecasting.historical_loader import HistoricalDataLoader
from app.forecasting.time_feature_extractor import TimeFeatureExtractor
from app.forecasting.dataset_builder import DatasetBuilder

from app.ml.random_forest_model import RandomForestModel
from app.ml.model_evaluator import ModelEvaluator
from app.ml.model_manager import ModelManager


class TrainingService:

    def __init__(self):

        self.loader = HistoricalDataLoader(
            "datasets/nasa_power/solar_history.csv"
        )

        self.extractor = TimeFeatureExtractor()

        self.builder = None

        self.trainer = RandomForestModel()

        self.evaluator = ModelEvaluator()

        self.manager = ModelManager()

    def train(self):

        dataset = self.loader.get_dataset()

        dataset = self.extractor.transform(dataset)

        self.builder = DatasetBuilder(dataset)

        X, y = self.builder.build_dataset()

        result = self.trainer.train(X, y)

        metrics = self.evaluator.evaluate(
            result["y_test"],
            result["predictions"]
        )

        model_path = self.manager.save_model(
            result["model"],
            "solar_random_forest.joblib"
        )

        return {
            "metrics": metrics,
            "model_path": model_path,
            "training_samples": len(result["X_train"]),
            "testing_samples": len(result["X_test"])
        }