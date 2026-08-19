from app.ml.model_manager import ModelManager
from app.ml.feature_schema import FeatureSchema

import pandas as pd


class ModelInference:

    def __init__(self):

        manager = ModelManager()

        self.model = manager.load_model(
            "solar_random_forest.joblib"
        )

    def predict(self, features):

        FeatureSchema.validate(features)

        dataframe = pd.DataFrame(
            [features],
            columns=FeatureSchema.FEATURES
        )

        prediction = self.model.predict(
            dataframe
        )

        return float(prediction[0])