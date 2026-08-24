class SoftConstraintScorer:
    """
    Calculates an overall feasibility score using
    non-mandatory site factors.
    """

    def __init__(self):
        self.weights = {
            "grid_distance": 0.40,
            "road_distance": 0.20,
            "solar_irradiance": 0.25,
            "wind_speed": 0.15
        }

    def normalize_inverse(self, value, maximum):
        """
        Higher distance = lower score.
        Returns a score between 0 and 100.
        """

        score = 100 * (1 - (value / maximum))

        return max(0, min(100, score))

    def normalize_direct(self, value, minimum, maximum):
        """
        Higher resource value = higher score.
        Returns a score between 0 and 100.
        """

        if value <= minimum:
            return 0

        if value >= maximum:
            return 100

        return (
            (value - minimum)
            / (maximum - minimum)
        ) * 100

    def calculate_score(self, features):

        grid_score = self.normalize_inverse(
            features["distance_to_grid"],
            20
        )

        road_score = self.normalize_inverse(
            features["distance_to_road"],
            10
        )

        solar_score = self.normalize_direct(
            features["solar_irradiance"],
            2,
            7
        )

        wind_score = self.normalize_direct(
            features["wind_speed"],
            2,
            10
        )

        overall_score = (
            grid_score * self.weights["grid_distance"]
            + road_score * self.weights["road_distance"]
            + solar_score * self.weights["solar_irradiance"]
            + wind_score * self.weights["wind_speed"]
        )

        return round(overall_score, 2)