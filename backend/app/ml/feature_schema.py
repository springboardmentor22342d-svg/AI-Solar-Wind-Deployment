"""
Feature Schema — the exact, ordered list of inputs the trained solar
energy model expects. Must match the FEATURE_COLUMNS used during
training (notebooks/12_prepare_training_data.py) exactly, in the
same order, or predictions will be silently wrong.
"""

SOLAR_MODEL_FEATURE_SCHEMA = [
    "solar_irradiance", "elevation", "slope", "forest_pct", "net_area_sown_pct",
    "fallow_land_pct", "culturable_wasteland_pct",
    "distance_to_road_km", "distance_to_grid_km",
    "distance_to_nearest_settlement_km", "nearby_settlement_count",
    "temperature", "humidity",
]


def build_model_input(features: dict) -> list:
    """
    Converts a FeatureBuilder-style dict into an ordered list matching
    SOLAR_MODEL_FEATURE_SCHEMA — the exact shape the model expects.
    """
    return [features.get(col) for col in SOLAR_MODEL_FEATURE_SCHEMA]