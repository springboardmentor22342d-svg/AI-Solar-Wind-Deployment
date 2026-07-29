from pathlib import Path
import csv
import json
import math

class RoadClient:
    """
    Accesses distance-to-nearest-road data using a simplified set of
    road sample points (major roads: motorway, trunk, primary),
    pre-processed from a full Overpass roads export — see
    notebooks/09_simplify_roads.py and dataset_summary.md.
    """

    BASE_DIR = Path(__file__).resolve().parents[3]
    ROADS_CSV = BASE_DIR / "datasets" / "openstreetmap" / "india_roads_simplified.csv"

    def __init__(self):
        with open(self.ROADS_CSV, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            self.points = [(float(row["lat"]), float(row["lon"])) for row in reader]

    def fetch(self, latitude: float, longitude: float) -> dict:
        km_per_deg_lat = 111.0
        km_per_deg_lon = 111.0 * math.cos(math.radians(latitude))
        avg_km_per_deg = (km_per_deg_lat + km_per_deg_lon) / 2

        min_dist_km = float("inf")
        for lat, lon in self.points:
            dist_deg = ((lat - latitude) ** 2 + (lon - longitude) ** 2) ** 0.5
            dist_km = dist_deg * avg_km_per_deg
            if dist_km < min_dist_km:
                min_dist_km = dist_km

        return {"distance_to_road_km": round(min_dist_km, 2)}


class GridClient:
    """
    Accesses distance-to-nearest-substation data (proxy for grid
    connection distance), from an Overpass substations export.
    """

    BASE_DIR = Path(__file__).resolve().parents[3]
    SUBSTATIONS_JSON = BASE_DIR / "datasets" / "openstreetmap" / "india_substations.json"

    def __init__(self):
        with open(self.SUBSTATIONS_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.points = []
        for element in data["elements"]:
            if "lat" in element and "lon" in element:
                self.points.append((element["lat"], element["lon"]))
            elif "center" in element:
                self.points.append((element["center"]["lat"], element["center"]["lon"]))

    def fetch(self, latitude: float, longitude: float) -> dict:
        km_per_deg_lat = 111.0
        km_per_deg_lon = 111.0 * math.cos(math.radians(latitude))
        avg_km_per_deg = (km_per_deg_lat + km_per_deg_lon) / 2

        min_dist_km = float("inf")
        for lat, lon in self.points:
            dist_deg = ((lat - latitude) ** 2 + (lon - longitude) ** 2) ** 0.5
            dist_km = dist_deg * avg_km_per_deg
            if dist_km < min_dist_km:
                min_dist_km = dist_km

        return {"distance_to_grid_km": round(min_dist_km, 2)}