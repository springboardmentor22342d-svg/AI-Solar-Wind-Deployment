import pytest

from backend.app.services.vector.processor import VectorProcessor


def test_vector_processor_can_be_created():
    processor = VectorProcessor()

    assert processor is not None


def test_load_vector_layer_is_not_implemented():
    processor = VectorProcessor()

    with pytest.raises(NotImplementedError):
        processor.load_vector_layer("roads.geojson")


def test_find_nearest_feature_is_not_implemented():
    processor = VectorProcessor()

    with pytest.raises(NotImplementedError):
        processor.find_nearest_feature(
            latitude=17.385,
            longitude=78.486
        )


def test_intersects_is_not_implemented():
    processor = VectorProcessor()

    with pytest.raises(NotImplementedError):
        processor.intersects(None)


def test_within_distance_is_not_implemented():
    processor = VectorProcessor()

    with pytest.raises(NotImplementedError):
        processor.within_distance(
            latitude=17.385,
            longitude=78.486,
            distance=10
        )