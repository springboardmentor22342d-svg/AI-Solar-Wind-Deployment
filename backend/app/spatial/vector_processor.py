import json
import math

class VectorProcessor:
    """
    Generic wrapper for point-based vector data (GeoJSON). Mirrors
    the settlement-distance logic already used in OsmClient, but
    generalized to work with any point-feature GeoJSON file.
    """

    def __init__(self, vector_path: str):
        self.vector_path = vector_path
        self._features = None

    def load_vector_layer(self):
        """Loads a GeoJSON file's point features into memory."""
        with open(self.vector_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self._features = []
        for feature in data["features"]:
            geom = feature["geometry"]
            if geom["type"] != "Point":
                continue  # this simple version handles point layers only
            lon, lat = geom["coordinates"]
            self._features.append({
                "lat": lat,
                "lon": lon,
                "properties": feature.get("properties", {}),
            })
        return self._features

    def _distance_km(self, lat1, lon1, lat2, lon2) -> float:
        km_per_deg_lat = 111.0
        km_per_deg_lon = 111.0 * math.cos(math.radians(lat1))
        avg_km_per_deg = (km_per_deg_lat + km_per_deg_lon) / 2
        dist_deg = ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5
        return dist_deg * avg_km_per_deg

    def find_nearest_feature(self, latitude: float, longitude: float):
        """Returns the closest feature to the given coordinate, with its distance."""
        if self._features is None:
            self.load_vector_layer()

        nearest = None
        min_dist = float("inf")
        for feature in self._features:
            dist = self._distance_km(latitude, longitude, feature["lat"], feature["lon"])
            if dist < min_dist:
                min_dist = dist
                nearest = feature

        if nearest is None:
            return None
        return {**nearest, "distance_km": round(min_dist, 2)}

    def intersects(self, latitude: float, longitude: float, tolerance_km: float = 0.1) -> bool:
        """
        For point layers, 'intersects' means 'is essentially at the
        same location as a feature' — checks within a small tolerance.
        """
        nearest = self.find_nearest_feature(latitude, longitude)
        return nearest is not None and nearest["distance_km"] <= tolerance_km

    def within_distance(self, latitude: float, longitude: float, distance_km: float) -> list:
        """Returns all features within the given distance of a coordinate."""
        if self._features is None:
            self.load_vector_layer()

        results = []
        for feature in self._features:
            dist = self._distance_km(latitude, longitude, feature["lat"], feature["lon"])
            if dist <= distance_km:
                results.append({**feature, "distance_km": round(dist, 2)})
        return results