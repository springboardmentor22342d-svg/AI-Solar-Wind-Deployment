import pytest

from backend.app.services.spatial_analysis import (
    SpatialAnalysisService
)


def test_spatial_analysis_service_can_be_created():
    service = SpatialAnalysisService()

    assert service is not None


def test_service_has_raster_processor():
    service = SpatialAnalysisService()

    assert service.raster_processor is not None


def test_service_has_vector_processor():
    service = SpatialAnalysisService()

    assert service.vector_processor is not None


def test_load_spatial_data_is_not_implemented():
    service = SpatialAnalysisService()

    with pytest.raises(NotImplementedError):
        service.load_spatial_data(
            raster_path="elevation.tif",
            vector_path="roads.geojson"
        )


def test_analyze_location_is_not_implemented():
    service = SpatialAnalysisService()

    with pytest.raises(NotImplementedError):
        service.analyze_location(
            latitude=17.385,
            longitude=78.486
        )


def test_calculate_suitability_is_not_implemented():
    service = SpatialAnalysisService()

    with pytest.raises(NotImplementedError):
        service.calculate_suitability(
            raster_values={
                "elevation": 540,
                "solar_irradiance": 5.8
            },
            vector_constraints=[]
        )