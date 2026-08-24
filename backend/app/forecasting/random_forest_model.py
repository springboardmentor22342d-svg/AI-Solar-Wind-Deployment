


import os
import joblib

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


class RandomForestForecastModel:

    def __init__(self):
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
        )

    def train(self, X, y):
        """
        Split the dataset, train the Random Forest,
        and return the train/test datasets.
        """

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42
        )

        self.model.fit(X_train, y_train)

        return X_train, X_test, y_train, y_test

    def save(self, model_path):
        directory = os.path.dirname(model_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        joblib.dump(self.model, model_path)

    def load(self, model_path):
        self.model = joblib.load(model_path)

    def predict(self, X):
        return self.model.predict(X)

    def get_feature_importance(self, feature_names):
        """
        Return feature importance in descending order.
        """

        importances = self.model.feature_importances_

        result = [
            {
                "feature": feature,
                "importance": float(importance)
            }
            for feature, importance in zip(
                feature_names,
                importances
            )
        ]

        result.sort(
            key=lambda item: item["importance"],
            reverse=True
        )

        return result

    def explain_prediction(self, feature_names, top_n=3):
        """
        Generate a concise explanation using the
        most influential features.
        """

        importance = self.get_feature_importance(
            feature_names
        )

        top_features = importance[:top_n]

        explanation_parts = []

        for item in top_features:
            explanation_parts.append(
                f"{item['feature']} "
                f"({item['importance']:.2f})"
            )

        explanation = (
            "The prediction is mainly influenced by: "
            + ", ".join(explanation_parts)
            + "."
        )

        return {
            "top_features": top_features,
            "explanation": explanation
        }
