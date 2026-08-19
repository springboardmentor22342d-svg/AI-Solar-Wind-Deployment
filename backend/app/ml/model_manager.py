import os
import joblib


class ModelManager:

    def __init__(self):

        self.model_directory = "models"

        os.makedirs(
            self.model_directory,
            exist_ok=True
        )

    def save_model(self, model, filename):

        path = os.path.join(
            self.model_directory,
            filename
        )

        joblib.dump(
            model,
            path
        )

        return path

    def load_model(self, filename):

        path = os.path.join(
            self.model_directory,
            filename
        )

        return joblib.load(path)