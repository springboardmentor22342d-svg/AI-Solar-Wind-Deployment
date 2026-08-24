

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor

from backend.app.forecasting.model_evaluation import (
    ModelEvaluator,
    create_comparison_table
)


def test_model_evaluation():

    X_train = pd.DataFrame({
        "temperature": [25, 26, 27, 28, 29, 30],
        "humidity": [50, 52, 54, 56, 58, 60]
    })

    y_train = [100, 110, 120, 130, 140, 150]

    X_validation = pd.DataFrame({
        "temperature": [31, 32, 33],
        "humidity": [62, 64, 66]
    })

    y_validation = [160, 170, 180]

    model = RandomForestRegressor(
        n_estimators=50,
        random_state=42
    )

    model.fit(
        X_train,
        y_train
    )

    results = ModelEvaluator.evaluate_regression(
        model,
        X_train,
        y_train,
        X_validation,
        y_validation
    )

    assert "train" in results
    assert "validation" in results

    assert "MAE" in results["validation"]
    assert "RMSE" in results["validation"]
    assert "R2" in results["validation"]


def test_compare_two_models():

    X_train = pd.DataFrame({
        "temperature": [25, 26, 27, 28, 29, 30],
        "humidity": [50, 52, 54, 56, 58, 60]
    })

    y_train = [100, 110, 120, 130, 140, 150]

    X_validation = pd.DataFrame({
        "temperature": [31, 32, 33],
        "humidity": [62, 64, 66]
    })

    y_validation = [160, 170, 180]

    models = {
        "Decision Tree": DecisionTreeRegressor(
            random_state=42
        ),

        "Random Forest": RandomForestRegressor(
            n_estimators=50,
            random_state=42
        )
    }

    results = {}

    for name, model in models.items():

        model.fit(
            X_train,
            y_train
        )

        results[name] = ModelEvaluator.evaluate_regression(
            model,
            X_train,
            y_train,
            X_validation,
            y_validation
        )

    comparison = create_comparison_table(
        results
    )

    assert len(comparison) == 2

    assert "Model" in comparison.columns
    assert "MAE" in comparison.columns
    assert "RMSE" in comparison.columns
    assert "R2" in comparison.columns
