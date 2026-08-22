import math
import rasterio

class RasterProcessor:
    """
    Generic wrapper for reading any single-band raster file.
    Unlike dataset-specific clients (SrtmClient, etc.), this class
    can be pointed at any .tif file, making it reusable across
    solar, wind, or elevation rasters.
    """

    def __init__(self, raster_path: str):
        self.raster_path = raster_path
        self._dataset = None

    def load_raster(self):
        """Opens the raster file and keeps the handle open for repeated sampling."""
        self._dataset = rasterio.open(self.raster_path)
        return self._dataset

    def sample_value(self, latitude: float, longitude: float):
        """
        Returns the pixel value at the given coordinate.
        Returns None if outside coverage or if the raster isn't loaded.
        """
        if self._dataset is None:
            self.load_raster()
        try:
            value = next(self._dataset.sample([(longitude, latitude)]))[0]
            value = float(value)
            return None if math.isnan(value) else value
        except Exception:
            return None

    def get_metadata(self) -> dict:
        """Returns CRS, dimensions, resolution, and nodata value."""
        if self._dataset is None:
            self.load_raster()
        return {
            "crs": str(self._dataset.crs),
            "width": self._dataset.width,
            "height": self._dataset.height,
            "resolution": self._dataset.res,
            "nodata": self._dataset.nodata,
        }

    def close(self):
        """Closes the raster file handle when done."""
        if self._dataset is not None:
            self._dataset.close()
            self._dataset = None