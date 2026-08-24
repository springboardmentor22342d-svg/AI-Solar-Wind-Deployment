# backend/app/evaluation/normalization.py


def normalize_positive(
    value: float,
    minimum: float,
    maximum: float
) -> float:

    if maximum <= minimum:
        raise ValueError(
            "Maximum must be greater than minimum."
        )

    if value <= minimum:
        return 0.0

    if value >= maximum:
        return 100.0

    score = (
        (value - minimum)
        / (maximum - minimum)
    ) * 100

    return round(score, 2)


def normalize_negative(
    value: float,
    minimum: float,
    maximum: float
) -> float:

    if maximum <= minimum:
        raise ValueError(
            "Maximum must be greater than minimum."
        )

    if value <= minimum:
        return 100.0

    if value >= maximum:
        return 0.0

    score = (
        (maximum - value)
        / (maximum - minimum)
    ) * 100

    return round(score, 2)


def normalize_solar_irradiance(
    solar_irradiance: float
) -> float:

    return normalize_positive(
        solar_irradiance,
        minimum=2.0,
        maximum=8.0
    )


def normalize_wind_speed(
    wind_speed: float
) -> float:

    return normalize_positive(
        wind_speed,
        minimum=2.0,
        maximum=10.0
    )


def normalize_slope(
    slope: float
) -> float:

    return normalize_negative(
        slope,
        minimum=0.0,
        maximum=30.0
    )


def normalize_distance_to_grid(
    distance: float
) -> float:

    return normalize_negative(
        distance,
        minimum=0.0,
        maximum=50.0
    )


def normalize_distance_to_road(
    distance: float
) -> float:

    return normalize_negative(
        distance,
        minimum=0.0,
        maximum=20.0
    )