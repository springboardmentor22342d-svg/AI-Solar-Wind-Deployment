class SpatialAnalysisService:
    """
    Coordinates raster and vector data sources into a single spatial
    analysis result. General-purpose wrapper around RasterProcessor/
    VectorProcessor instances, complementing FeatureBuilder's
    dataset-specific pipeline.
    """

    def __init__(self, raster_processors: dict, vector_processors: dict):
        """
        raster_processors: dict of {layer_name: RasterProcessor}
        vector_processors: dict of {layer_name: VectorProcessor}
        """
        self.raster_processors = raster_processors
        self.vector_processors = vector_processors

    def analyze_location(self, latitude: float, longitude: float) -> dict:
        """
        Samples every configured raster and finds the nearest feature
        in every configured vector layer, for a given coordinate.
        Returns a combined dict of all layer results.
        """
        result = {}

        for layer_name, processor in self.raster_processors.items():
            result[layer_name] = processor.sample_value(latitude, longitude)

        for layer_name, processor in self.vector_processors.items():
            nearest = processor.find_nearest_feature(latitude, longitude)
            result[f"{layer_name}_nearest"] = nearest

        return result