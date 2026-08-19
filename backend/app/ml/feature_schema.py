class FeatureSchema:

    FEATURES = [
        "month",
        "day",
        "day_of_year",
        "week_of_year",
        "temperature",
        "humidity",
        "wind_speed"
    ]

    @classmethod
    def validate(cls, features):

        if len(features) != len(cls.FEATURES):

            raise ValueError(
                f"Expected {len(cls.FEATURES)} features but received {len(features)}."
            )

        for value in features:

            if not isinstance(value, (int, float)):

                raise ValueError(
                    "All feature values must be numeric."
                )

        return True