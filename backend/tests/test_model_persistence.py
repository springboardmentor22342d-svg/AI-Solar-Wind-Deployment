from sklearn.ensemble import RandomForestRegressor

from backend.app.forecasting.model_persistence import (
    ModelPersistence
)


def test_save_and_load_model():

    model = RandomForestRegressor()

    persistence = ModelPersistence(
        "models/test_model.pkl"
    )

    persistence.save_model(
        model
    )

    loaded_model = persistence.load_model()

    assert loaded_model is not None