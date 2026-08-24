import pytest

from backend.app.services.raster.processor import RasterProcessor


def test_raster_processor_can_be_created():
    processor = RasterProcessor()

    assert processor is not None


def test_get_metadata_returns_dictionary():
    processor = RasterProcessor()

    metadata = processor.get_metadata()

    assert isinstance(metadata, dict)


def test_load_raster_is_not_implemented():
    processor = RasterProcessor()

    with pytest.raises(NotImplementedError):
        processor.load_raster("sample.tif")


def test_sample_value_is_not_implemented():
    processor = RasterProcessor()

    with pytest.raises(NotImplementedError):
        processor.sample_value(17.385, 78.486)