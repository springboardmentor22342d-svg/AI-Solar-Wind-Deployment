import pytest
from app.ml.model_inference import ModelInference

def test_model_inference_valid():
    model = ModelInference()
    prediction = model.predict([7, 15, 196, 28, 31.2, 62.0, 3.5])
    assert isinstance(prediction, float)

def test_model_inference_invalid():
    model = ModelInference()
    with pytest.raises(ValueError):
        model.predict([7, "hello", 196, 28, 31.2, 62.0, 3.5])