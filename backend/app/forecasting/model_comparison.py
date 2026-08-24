import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


class ModelComparison:

    def evaluate(self, model, X_valid, y_valid):
        """
        Evaluate a regression model.
        """

        predictions = model.predict(X_valid)

        mae = mean_absolute_error(
            y_valid,
            predictions
        )

        rmse = mean_squared_error(
            y_valid,
            predictions
        ) ** 0.5

        r2 = r2_score(
            y_valid,
            predictions
        )

        return {
            "MAE": mae,
            "RMSE": rmse,
            "R2 Score": r2
        }

    def compare(
        self,
        decision_tree,
        random_forest,
        X_valid,
        y_valid
    ):

        dt = self.evaluate(
            decision_tree,
            X_valid,
            y_valid
        )

        rf = self.evaluate(
            random_forest,
            X_valid,
            y_valid
        )

        table = pd.DataFrame([
            {
                "Model": "Decision Tree",
                **dt
            },
            {
                "Model": "Random Forest",
                **rf
            }
        ])

        return table