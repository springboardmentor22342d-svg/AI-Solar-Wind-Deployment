from app.evaluation.weights import *


# -----------------------------
# Normalization Functions
# -----------------------------

def normalize_solar(irradiance):
    """
    Solar Irradiance: 3 - 7 kWh/m²/day
    Higher is better
    """
    min_val = 3
    max_val = 7

    score = ((irradiance - min_val) / (max_val - min_val)) * 100

    return max(0, min(score, 100))


def normalize_wind(speed):
    """
    Wind Speed: 2 - 12 m/s
    Higher is better
    """
    min_val = 2
    max_val = 12

    score = ((speed - min_val) / (max_val - min_val)) * 100

    return max(0, min(score, 100))


def normalize_slope(slope):
    """
    Lower slope is better
    """
    min_val = 0
    max_val = 30

    score = ((max_val - slope) / (max_val - min_val)) * 100

    return max(0, min(score, 100))


def normalize_grid(distance):
    """
    Smaller distance to grid is better
    """
    min_val = 0
    max_val = 20

    score = ((max_val - distance) / (max_val - min_val)) * 100

    return max(0, min(score, 100))


def normalize_road(distance):
    """
    Smaller distance to road is better
    """
    min_val = 0
    max_val = 20

    score = ((max_val - distance) / (max_val - min_val)) * 100

    return max(0, min(score, 100))


# -----------------------------
# Category Scores
# -----------------------------

def renewable_resource_score(feature):

    solar = feature["solar"]

    if isinstance(solar, dict):
        solar = sum(solar.values()) / len(solar)

    solar_score = normalize_solar(solar)
    wind_score = normalize_wind(feature["wind"])

    return round((solar_score + wind_score) / 2, 2)


def terrain_score(feature):
    return round(normalize_slope(feature["slope"]), 2)


def infrastructure_score(feature):

    grid = normalize_grid(feature["grid"])
    road = normalize_road(feature["road"])

    return round((grid + road) / 2, 2)


def environmental_score(feature):
    """
    Placeholder score.
    """
    return 100


def economic_score(feature):
    """
    Uses infrastructure as economic indicator.
    """
    return infrastructure_score(feature)


# -----------------------------
# Overall Site Score
# -----------------------------

def calculate_score(feature):

    solar = feature["solar"]

    if isinstance(solar, dict):
        solar = sum(solar.values()) / len(solar)

    solar_score = normalize_solar(solar)
    wind_score = normalize_wind(feature["wind"])
    slope_score = normalize_slope(feature["slope"])
    grid_score = normalize_grid(feature["grid"])
    road_score = normalize_road(feature["road"])

    overall_score = (
        solar_score * SOLAR_WEIGHT +
        wind_score * WIND_WEIGHT +
        slope_score * SLOPE_WEIGHT +
        grid_score * GRID_WEIGHT +
        road_score * ROAD_WEIGHT
    )

    return round(overall_score, 2)