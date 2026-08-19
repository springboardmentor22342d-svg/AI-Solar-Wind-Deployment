from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error
)

import numpy as np


class ModelEvaluator:

    def evaluate(self, y_true, predictions):

        mae = mean_absolute_error(
            y_true,
            predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                y_true,
                predictions
            )
        )

        r2 = r2_score(
            y_true,
            predictions
        )

        mape = mean_absolute_percentage_error(
            y_true,
            predictions
        ) * 100

        return {

            "MAE": round(mae, 4),

            "RMSE": float(round(rmse, 4)),

            "R2": round(r2, 4),

            "MAPE": round(mape, 2)

        }