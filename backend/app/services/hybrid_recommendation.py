


def recommend_hybrid_strategy(
    solar_class: str,
    wind_class: str
) -> str:

    if (
        solar_class in ["Good", "Excellent"]
        and wind_class in ["Good", "Excellent"]
    ):
        return "Hybrid"

    elif solar_class in ["Good", "Excellent"]:
        return "Solar"

    elif wind_class in ["Good", "Excellent"]:
        return "Wind"

    else:
        return "Not Recommended"