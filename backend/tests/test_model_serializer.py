from sklearn.ensemble import RandomForestRegressor

from backend.app.forecasting.model_serializer import (
    ModelSerializer
)


def test_save_and_load():

    model = RandomForestRegressor()

    serializer = ModelSerializer(
        "models/test_model.pkl"
    )

    serializer.save(model)

    loaded_model = serializer.load()

    assert loaded_model is not None