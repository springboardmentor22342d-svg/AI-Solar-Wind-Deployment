class TerrainService:
    """
    Terrain analysis service.

    This service provides terrain-related features
    for the site analysis pipeline.

    Real DEM/SRTM integration can be connected later.
    """

    def __init__(self):
        pass

    def analyze(
        self,
        latitude: float,
        longitude: float
    ):
        """
        Return terrain features for a location.

        Currently returns default values because
        DEM/SRTM data is not connected yet.
        """

        return {
            "elevation": 0.0,
            "slope": 0.0,
            "terrain_class": "Unknown"
        }