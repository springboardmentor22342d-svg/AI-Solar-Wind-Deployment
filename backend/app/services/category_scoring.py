from app.services.score_normalizer import ScoreNormalizer


class CategoryScoringService:
    """
    Computes category-wise scores for
    site suitability evaluation.
    """

    def __init__(self):
        self.normalizer = ScoreNormalizer()

    def renewable_resource_score(
        self,
        solar_irradiance: float,
        wind_speed: float,
    ):
        """
        Renewable Resource Score
        (Solar + Wind)
        """

        solar_score = self.normalizer.normalize_solar(
            solar_irradiance
        )

        wind_score = self.normalizer.normalize_wind(
            wind_speed
        )

        return round(
            (solar_score + wind_score) / 2,
            2
        )

    def terrain_score(
        self,
        slope: float,
        elevation: float,
    ):
        """
        Terrain Score
        (Slope + Elevation)
        """

        slope_score = self.normalizer.normalize_slope(
            slope
        )

        elevation_score = max(
            0,
            min(
                100,
                100 - (elevation / 3000) * 100
            )
        )

        return round(
            (slope_score + elevation_score) / 2,
            2
        )

    def infrastructure_score(
        self,
        distance_to_road: float,
        distance_to_grid: float,
    ):
        """
        Infrastructure Score
        """

        road_score = self.normalizer.normalize_road_distance(
            distance_to_road
        )

        grid_score = self.normalizer.normalize_grid_distance(
            distance_to_grid
        )

        return round(
            (road_score + grid_score) / 2,
            2
        )

    def environmental_score(
        self,
        environmental_rating: float,
    ):
        """
        Environmental Score

        Expected range:
        0 - 100
        """

        return round(
            max(
                0,
                min(environmental_rating, 100)
            ),
            2
        )

    def economic_score(
        self,
        economic_rating: float,
    ):
        """
        Economic Score

        Expected range:
        0 - 100
        """

        return round(
            max(
                0,
                min(economic_rating, 100)
            ),
            2
        )