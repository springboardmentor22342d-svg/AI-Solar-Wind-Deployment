from pathlib import Path
import json
import math

class OsmClient:
    """
    Accesses OpenStreetMap-derived settlement data. Loads the
    towns/cities GeoJSON once at startup, not on every fetch call.
    """

    BASE_DIR = Path(__file__).resolve().parents[3]
    TOWNS_GEOJSON = BASE_DIR / "datasets" / "openstreetmap" / "osm-india-cities-towns.geojson"

    def __init__(self):
        with open(self.TOWNS_GEOJSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.towns = []
        for feature in data["features"]:
            props = feature["properties"]
            lon, lat = feature["geometry"]["coordinates"]
            self.towns.append({"name": props.get("name", "unknown"), "lat": lat, "lon": lon})

    def fetch(self, latitude: float, longitude: float, radius_km: float = 30) -> dict:
        km_per_deg_lat = 111.0
        km_per_deg_lon = 111.0 * math.cos(math.radians(latitude))
        avg_km_per_deg = (km_per_deg_lat + km_per_deg_lon) / 2

        nearby_count = 0
        min_dist_km = float("inf")
        nearest_name = None

        for town in self.towns:
            dist_deg = ((town["lat"] - latitude) ** 2 + (town["lon"] - longitude) ** 2) ** 0.5
            dist_km = dist_deg * avg_km_per_deg
            if dist_km < min_dist_km:
                min_dist_km = dist_km
                nearest_name = town["name"]
            if dist_km <= radius_km:
                nearby_count += 1

        return {
            "nearby_settlement_count": nearby_count,
            "distance_to_nearest_settlement_km": round(min_dist_km, 2),
            "nearest_settlement_name": nearest_name,
        }