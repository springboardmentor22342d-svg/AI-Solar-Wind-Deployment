from pathlib import Path
import math
import rasterio

class SrtmClient:
    """
    Accesses elevation via a real SRTM raster (90m resolution),
    downloaded directly from OpenTopography (official SRTM distributor).
    Replaces the earlier district-level CSV approximation, which was
    too coarse to compute meaningful slope (see dataset_summary.md).

    Coverage: India, south of 34°N (excludes the far-northern disputed
    border strip — consistent with existing exclusions in the Feature
    Store, see dataset_summary.md).
    """

    BASE_DIR = Path(__file__).resolve().parents[3]
    ELEVATION_TIF = BASE_DIR / "datasets" / "srtm" / "india_elevation.tif"

    def fetch(self, latitude: float, longitude: float) -> dict:
        try:
            with rasterio.open(self.ELEVATION_TIF) as src:
                value = next(src.sample([(longitude, latitude)]))[0]
                value = float(value)
                return {"elevation": None if math.isnan(value) else value}
        except Exception:
            return {"elevation": None}

    def fetch_slope(self, latitude: float, longitude: float, offset_deg: float = 0.001) -> dict:
        """
        offset_deg=0.001 (~111m) is appropriate for a 90m-resolution
        raster — compares genuinely adjacent pixels, unlike the old
        district-level approach which compared across huge districts.
        """
        try:
            center = self.fetch(latitude, longitude)["elevation"]
            north = self.fetch(latitude + offset_deg, longitude)["elevation"]
            south = self.fetch(latitude - offset_deg, longitude)["elevation"]
            east = self.fetch(latitude, longitude + offset_deg)["elevation"]
            west = self.fetch(latitude, longitude - offset_deg)["elevation"]

            distance_m = offset_deg * 111_000
            diffs = [abs(center - v) for v in [north, south, east, west] if v is not None and center is not None]

            if not diffs:
                return {"slope": None}

            max_diff = max(diffs)
            slope_degrees = math.degrees(math.atan(max_diff / distance_m))
            return {"slope": round(slope_degrees, 2)}
        except Exception:
            return {"slope": None}