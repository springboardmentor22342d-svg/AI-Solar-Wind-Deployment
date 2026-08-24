

import os

import joblib
import pandas as pd


class ModelInference:
    """
    Load a serialized ML model and perform predictions.

    The model is loaded once when the class is initialized.
    No model training occurs during inference.
    """

    REQUIRED_FEATURES = [
        "temperature",
        "humidity",
        "wind_speed",
        "solar_irradiance",
        "year",
        "month",
        "day",
        "day_of_year"
       
    ]

    def __init__(self, model_path="models/best_model.pkl"):
        """
        Load the serialized model.
        """

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {model_path}"
            )

        self.model = joblib.load(model_path)

    def predict(self, features):
        """
        Generate a prediction using the loaded model.

        Parameters
        ----------
        features : dict
            Input features required by the model.

        Returns
        -------
        list
            Model prediction.
        """

        # Check required features
        missing_features = [
            feature
            for feature in self.REQUIRED_FEATURES
            if feature not in features
        ]

        if missing_features:
            raise ValueError(
                f"Missing required features: "
                f"{missing_features}"
            )

        # Create DataFrame in the exact training order
        input_data = pd.DataFrame(
            [[
                features[feature]
                for feature in self.REQUIRED_FEATURES
            ]],
            columns=self.REQUIRED_FEATURES
        )

        # Predict without retraining
        prediction = self.model.predict(
            input_data
        )

        return prediction.tolist()