from pathlib import Path
import math
import rasterio

class GlobalSolarAtlasClient:
    """
    Accesses Global Solar Atlas solar rasters (GHI, GTI, OPTA).
    Renamed from NasaPowerClient to avoid collision with the new
    live NASA POWER API client (see nasa_power.py).
    """
    BASE_DIR = Path(__file__).resolve().parents[3]
    SOLAR_DIR = BASE_DIR / "datasets" / "nasa_power"

    def fetch(self, latitude: float, longitude: float) -> dict:
        values = {}
        for param in ["GHI", "GTI", "OPTA"]:
            path = self.SOLAR_DIR / f"{param}.tif"
            try:
                with rasterio.open(path) as src:
                    value = next(src.sample([(longitude, latitude)]))[0]
                    value = float(value)
                    values[param.lower()] = None if math.isnan(value) else value
            except Exception:
                values[param.lower()] = None
        return values