from backend.app.forecasting.model_analysis import ModelAnalysis


def test_underfitting():

    analysis = ModelAnalysis()

    result = analysis.analyze(
        train_r2=0.55,
        validation_r2=0.52
    )

    assert result == "Underfitting"


def test_overfitting():

    analysis = ModelAnalysis()

    result = analysis.analyze(
        train_r2=0.98,
        validation_r2=0.70
    )

    assert result == "Overfitting"


def test_generalization():

    analysis = ModelAnalysis()

    result = analysis.analyze(
        train_r2=0.91,
        validation_r2=0.88
    )

    assert result == "Generalizing Well"