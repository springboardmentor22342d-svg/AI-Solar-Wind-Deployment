class RasterProcessor:
    def load_raster(self,path: str):
        """
        Load raster file.
        """
        raise NotImplementedError
    def sample_value(self,latitude: float,longitude: float):
        """
        Sample raster value.
        """
        raise NotImplementedError
    def get_metadata(self):
        """
        Return raster metadata.
        """
        return NotImplementedError