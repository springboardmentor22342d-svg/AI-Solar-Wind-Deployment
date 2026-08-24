import joblib
from pathlib import Path


class ModelSerializer:

    def __init__(self, model_path="models/best_model.pkl"):

        self.model_path = Path(model_path)

        self.model_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def save(self, model):

        joblib.dump(
            model,
            self.model_path
        )

        print(
            f"Model saved to {self.model_path}"
        )

    def load(self):

        if not self.model_path.exists():
            raise FileNotFoundError(
                "Saved model not found."
            )

        return joblib.load(
            self.model_path
        )