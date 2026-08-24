from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

from backend.app.forecasting.baseline_models import BaselineModels
from backend.app.forecasting.model_comparison import ModelComparison


def test_compare_models():

    X, y = make_regression(
        n_samples=200,
        n_features=5,
        random_state=42
    )

    X_train, X_valid, y_train, y_valid = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42
    )

    trainer = BaselineModels()

    decision_tree = trainer.train_decision_tree(
        X_train,
        y_train
    )

    random_forest = trainer.train_random_forest(
        X_train,
        y_train
    )

    comparison = ModelComparison()

    results = comparison.compare(
        decision_tree,
        random_forest,
        X_valid,
        y_valid
    )

    assert len(results) == 2
    assert "MAE" in results.columns
    assert "RMSE" in results.columns
    assert "R2 Score" in results.columns