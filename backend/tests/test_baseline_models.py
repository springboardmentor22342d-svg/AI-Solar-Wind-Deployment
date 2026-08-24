from sklearn.datasets import make_regression

from backend.app.forecasting.baseline_models import (
    BaselineModels
)


def test_train_models():

    X, y = make_regression(
        n_samples=100,
        n_features=4,
        random_state=42
    )

    trainer = BaselineModels()

    dt_model = trainer.train_decision_tree(
        X,
        y
    )

    rf_model = trainer.train_random_forest(
        X,
        y
    )

    assert dt_model is not None
    assert rf_model is not None
    