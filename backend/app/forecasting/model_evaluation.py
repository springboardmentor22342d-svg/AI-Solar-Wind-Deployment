import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


class ModelEvaluator:
    """
    Evaluate regression and forecasting models.
    """

    @staticmethod
    def calculate_metrics(y_true, y_pred):
        """
        Calculate regression metrics.
        """

        mae = mean_absolute_error(
            y_true,
            y_pred
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_true,
                y_pred
            )
        )

        r2 = r2_score(
            y_true,
            y_pred
        )

        # MAPE
        y_true_array = np.asarray(y_true)
        y_pred_array = np.asarray(y_pred)

        non_zero = y_true_array != 0

        if np.any(non_zero):
            mape = np.mean(
                np.abs(
                    (
                        y_true_array[non_zero]
                        - y_pred_array[non_zero]
                    )
                    / y_true_array[non_zero]
                )
            ) * 100
        else:
            mape = np.nan

        return {
            "MAE": mae,
            "RMSE": rmse,
            "R2": r2,
            "MAPE": mape
        }

    @staticmethod
    def evaluate_regression(
        model,
        X_train,
        y_train,
        X_validation,
        y_validation
    ):
        """
        Evaluate a trained regression model
        on training and validation datasets.
        """

        # Training predictions
        train_predictions = model.predict(X_train)

        # Validation predictions
        validation_predictions = model.predict(
            X_validation
        )

        # Calculate training metrics
        train_metrics = ModelEvaluator.calculate_metrics(
            y_train,
            train_predictions
        )

        # Calculate validation metrics
        validation_metrics = ModelEvaluator.calculate_metrics(
            y_validation,
            validation_predictions
        )

        return {
            "train": train_metrics,
            "validation": validation_metrics
        }


def create_comparison_table(results):
    """
    Create a model comparison table.

    Parameters
    ----------
    results : dict
        Dictionary containing model names and
        evaluation results.

    Returns
    -------
    pandas.DataFrame
    """

    rows = []

    for model_name, result in results.items():

        validation = result["validation"]

        rows.append({
            "Model": model_name,
            "MAE": validation["MAE"],
            "RMSE": validation["RMSE"],
            "R2": validation["R2"],
            "MAPE": validation["MAPE"]
        })

    return pd.DataFrame(rows)