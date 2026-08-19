class ScoreNormalizer:
    """
    Normalize different parameters onto
    a common 0–100 scoring scale.
    """

    def normalize_solar(
        self,
        solar_irradiance: float,
    ):
        """
        Solar Irradiance (0 - 8 kWh/m²/day)
        Higher is better.
        """

        score = (solar_irradiance / 8.0) * 100

        return round(
            max(0, min(score, 100)),
            2
        )

    def normalize_wind(
        self,
        wind_speed: float,
    ):
        """
        Wind Speed (0 - 12 m/s)
        Higher is better.
        """

        score = (wind_speed / 12.0) * 100

        return round(
            max(0, min(score, 100)),
            2
        )

    def normalize_slope(
        self,
        slope: float,
    ):
        """
        Slope (0° - 30°)

        Lower slope is better.
        """

        score = 100 - ((slope / 30.0) * 100)

        return round(
            max(0, min(score, 100)),
            2
        )

    def normalize_grid_distance(
        self,
        distance: float,
    ):
        """
        Distance to Grid (0 - 20 km)

        Smaller distance is better.
        """

        score = 100 - ((distance / 20.0) * 100)

        return round(
            max(0, min(score, 100)),
            2
        )

    def normalize_road_distance(
        self,
        distance: float,
    ):
        """
        Distance to Road (0 - 10 km)

        Smaller distance is better.
        """

        score = 100 - ((distance / 10.0) * 100)

        return round(
            max(0, min(score, 100)),
            2
        )