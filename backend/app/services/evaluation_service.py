from app.spatial.spatial_service import SpatialAnalysisService
from app.evaluation.evaluator import Evaluator


class EvaluationService:

    def __init__(self):
        self.spatial = SpatialAnalysisService()

    def evaluate_features(
        self,
        feature_vector: dict
    ):
        """
        Evaluate an already generated feature vector.
        """

        return Evaluator.evaluate(
            site_id=1,
            features=feature_vector
        )

    def evaluate_site(
        self,
        latitude: float,
        longitude: float
    ):
        """
        Backward compatible method.
        Generates features and evaluates them.
        """

        feature_vector = self.spatial.suitability_pipeline(
            latitude,
            longitude
        )

        return self.evaluate_features(
            feature_vector
        )