from typing import Any, Dict, Optional


class RasterProcessor:
    """
    Skeleton class for raster data processing.

    This class will later be responsible for:
    - Loading raster datasets
    - Sampling raster values using latitude and longitude
    - Returning raster metadata

    Real raster processing is not implemented yet.
    """

    def __init__(self):
        """
        Initialize the RasterProcessor.

        The raster dataset is initially empty because this task
        focuses only on API design.
        """

        self.raster_data: Optional[Any] = None
        self.metadata: Dict[str, Any] = {}

    def load_raster(self, file_path: str) -> None:
        """
        Load a raster dataset.

        Args:
            file_path: Path to the raster file.

        Raises:
            NotImplementedError:
                Real raster loading will be implemented later.
        """

        raise NotImplementedError(
            "Raster loading is not implemented yet."
        )

    def sample_value(
        self,
        latitude: float,
        longitude: float
    ) -> Optional[float]:
        """
        Sample a raster value at a geographic coordinate.

        Args:
            latitude: Geographic latitude.
            longitude: Geographic longitude.

        Returns:
            The raster value at the specified coordinate.

        Raises:
            NotImplementedError:
                Real raster sampling will be implemented later.
        """

        raise NotImplementedError(
            "Raster value sampling is not implemented yet."
        )

    def get_metadata(self) -> Dict[str, Any]:
        """
        Return metadata about the loaded raster.

        Returns:
            Dictionary containing raster metadata.
        """

        return self.metadata