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

WIND_MODEL_FEATURE_SCHEMA = [
    "wind_speed", "elevation", "slope", "forest_pct", "net_area_sown_pct",
    "fallow_land_pct", "culturable_wasteland_pct",
    "distance_to_road_km", "distance_to_grid_km",
    "distance_to_nearest_settlement_km", "nearby_settlement_count",
    "temperature", "humidity",
]


def build_model_input(features: dict, schema: list) -> list:
    return [features.get(col) for col in schema]


# Pre-computed feature importance (top contributors), from
# notebooks/19_feature_importance.py — used to generate concise,
# human-readable explanations alongside predictions.
SOLAR_TOP_FEATURES = ["solar_irradiance", "distance_to_road_km", "elevation"]
WIND_TOP_FEATURES = ["wind_speed", "nearby_settlement_count", "humidity"]


def build_explanation(features: dict, top_features: list, primary_driver_label: str) -> str:
    """
    Builds a concise, human-readable explanation of what drove a
    prediction, based on the model's known top-contributing features.
    """
    primary_value = features.get(top_features[0])
    if primary_value is None:
        return "Explanation unavailable — primary driver feature missing."

    return (
        f"Prediction primarily driven by {primary_driver_label} "
        f"({primary_value:.2f}), which accounts for the vast majority "
        f"of the model's decision. Secondary factors ({', '.join(top_features[1:])}) "
        f"contributed minor adjustments."
    )