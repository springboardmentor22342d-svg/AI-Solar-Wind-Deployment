class RasterProcessor:

    """
    Skeleton class for raster operations.

    Future datasets:
    - NASA POWER
    - SRTM
    - Raster TIFF files

    """

    def __init__(self):
        self.raster = None

    def load_raster(self, raster_path: str):
        """
        Load raster dataset.

        Parameters:
            raster_path (str)

        Returns:
            None
        """

        print(f"Loading raster: {raster_path}")

    def sample_value(self, latitude: float, longitude: float):
        """
        Sample raster value.

        Parameters:
            latitude
            longitude

        Returns:
            float
        """

        print(
            f"Sampling raster at ({latitude}, {longitude})"
        )

        return None

    def get_metadata(self):
        """
        Return raster metadata.

        Returns:
            dict
        """

        metadata = {
            "crs": "EPSG:4326",
            "resolution": None,
            "width": None,
            "height": None,
        }

        return metadata