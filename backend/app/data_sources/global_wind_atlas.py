from pathlib import Path
import math
import rasterio

class GlobalWindAtlasClient:
    """
    Accesses Global Wind Atlas rasters (wind speed, power density @ 100m).
    """

    BASE_DIR = Path(__file__).resolve().parents[3]
    WIND_DIR = BASE_DIR / "datasets" / "global_wind_atlas"
    FILES = {
        "wind_speed_100m": "wind_speed_100m.tif",
        "power_density_100m": "power_density_100m.tif",
    }

    def __init__(self):
        self.datasets = {}
        for key, filename in self.FILES.items():
            path = self.WIND_DIR / filename
            try:
                self.datasets[key] = rasterio.open(path)
            except Exception:
                self.datasets[key] = None

    def fetch(self, latitude: float, longitude: float) -> dict:
        values = {}
        for key in self.FILES:
            src = self.datasets.get(key)
            try:
                if src is None:
                    values[key] = None
                    continue
                value = next(src.sample([(longitude, latitude)]))[0]
                value = float(value)
                values[key] = None if math.isnan(value) else value
            except Exception:
                # Coordinate outside coverage (e.g. disputed border regions)
                values[key] = None
        return values

    def close(self):
        for src in self.datasets.values():
            if src is not None:
                src.close()
