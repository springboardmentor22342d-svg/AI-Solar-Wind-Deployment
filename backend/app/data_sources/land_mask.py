"""
Land/water mask — determines whether a coordinate falls on land or
in open water (ocean, large lakes), using Natural Earth's public
domain 50m land polygon dataset. This closes a real gap: without
this check, coordinates in open water could otherwise pass through
the analysis pipeline and receive a misleading suitability score.
"""

from pathlib import Path
import shapefile
from shapely.geometry import shape, Point


class LandMaskClient:
    BASE_DIR = Path(__file__).resolve().parents[3]
    LAND_SHP = BASE_DIR / "datasets" / "land_mask" / "ne_50m_land.shp"

    def __init__(self):
        sf = shapefile.Reader(str(self.LAND_SHP))
        # Build shapely geometries once, at startup — reused for
        # every is_on_land() call rather than re-parsing the shapefile
        self.land_polygons = [shape(s.__geo_interface__) for s in sf.shapes()]

    def is_on_land(self, latitude: float, longitude: float) -> bool:
        point = Point(longitude, latitude)
        for polygon in self.land_polygons:
            if polygon.contains(point):
                return True
        return False