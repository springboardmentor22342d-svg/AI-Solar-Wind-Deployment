
import os
import joblib


class ModelPersistence:
    """
    Save and load trained machine learning models.
    """

    def __init__(self, model_path):
        self.model_path = model_path

    def save_model(self, model):
        """
        Save a trained model using joblib.
        """

        # Create directory if it does not exist
        directory = os.path.dirname(self.model_path)

        if directory:
            os.makedirs(
                directory,
                exist_ok=True
            )

        joblib.dump(
            model,
            self.model_path
        )

        return self.model_path

    def load_model(self):
        """
        Load a previously saved model.
        """

        if not os.path.exists(
            self.model_path
        ):
            raise FileNotFoundError(
                f"Model file not found: "
                f"{self.model_path}"
            )

        return joblib.load(
            self.model_path
        )