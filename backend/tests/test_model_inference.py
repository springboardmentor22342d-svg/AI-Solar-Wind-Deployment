from backend.app.inference.model_inference import ModelInference


def test_model_prediction():

    model = ModelInference(
        "models/best_model.pkl"
    )

    features = {
        "temperature": 29,
        "humidity": 60,
        "wind_speed": 6.8,
      "solar_irradiance": 5.5,
        "year": 2026,
        "month": 8,
        "day": 1,
        "day_of_year": 213,
        "week": 31
    }

    prediction = model.predict(
        features
    )

    assert prediction is not None
    assert isinstance(prediction, list)
    assert len(prediction) == 1

    assert isinstance(
        prediction[0],
        (int, float)
    )