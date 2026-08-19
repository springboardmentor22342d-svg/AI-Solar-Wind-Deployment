"""
Constraint Validation Module
"""

MAX_SLOPE = 15

MIN_SOLAR_IRRADIANCE = 5.0

MIN_WIND_SPEED = 5.5

MAX_GRID_DISTANCE = 5.0

MAX_ROAD_DISTANCE = 3.0


def validate_slope(slope: float):

    return slope <= MAX_SLOPE


def validate_solar(solar: float):

    return solar >= MIN_SOLAR_IRRADIANCE


def validate_wind(wind: float):

    return wind >= MIN_WIND_SPEED


def validate_grid_distance(distance: float):

    return distance <= MAX_GRID_DISTANCE


def validate_road_distance(distance: float):

    return distance <= MAX_ROAD_DISTANCE


def evaluate_constraints(features: dict):

    return {

        "solar": validate_solar(features["solar_irradiance"]),

        "wind": validate_wind(features["wind_speed"]),

        "slope": validate_slope(features["slope"]),

        "grid_distance": validate_grid_distance(
            features["distance_to_grid"]
        ),

        "road_distance": validate_road_distance(
            features["distance_to_road"]
        )

    }