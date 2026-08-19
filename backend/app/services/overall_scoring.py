from app.services.category_scoring import CategoryScoringService


class OverallScoringService:
    """
    Calculates the overall site suitability
    score using weighted category scores.
    """

    def __init__(self):
        self.category_service = CategoryScoringService()

        self.weights = {
            "resource": 0.35,
            "terrain": 0.25,
            "infrastructure": 0.15,
            "environmental": 0.15,
            "economic": 0.10,
        }

    def calculate_overall_score(
        self,
        solar_irradiance: float,
        wind_speed: float,
        slope: float,
        elevation: float,
        distance_to_road: float,
        distance_to_grid: float,
        environmental_rating: float,
        economic_rating: float,
    ):

        resource_score = self.category_service.renewable_resource_score(
            solar_irradiance,
            wind_speed,
        )

        terrain_score = self.category_service.terrain_score(
            slope,
            elevation,
        )

        infrastructure_score = self.category_service.infrastructure_score(
            distance_to_road,
            distance_to_grid,
        )

        environmental_score = self.category_service.environmental_score(
            environmental_rating
        )

        economic_score = self.category_service.economic_score(
            economic_rating
        )

        overall_score = (
            resource_score * self.weights["resource"]
            + terrain_score * self.weights["terrain"]
            + infrastructure_score * self.weights["infrastructure"]
            + environmental_score * self.weights["environmental"]
            + economic_score * self.weights["economic"]
        )

        return {
            "resource_score": round(resource_score, 2),
            "terrain_score": round(terrain_score, 2),
            "infrastructure_score": round(infrastructure_score, 2),
            "environmental_score": round(environmental_score, 2),
            "economic_score": round(economic_score, 2),
            "overall_score": round(overall_score, 2),
        }
    def calculate_from_features(
        self,
        feature_vector: dict,
    ):
        """
        Calculate overall score directly from
        a feature vector.
        """

        return self.calculate_overall_score(
            solar_irradiance=feature_vector["solar_irradiance"],
            wind_speed=feature_vector["wind_speed"],
            slope=feature_vector["slope"],
            elevation=feature_vector["elevation"],
            distance_to_road=feature_vector["distance_to_road"],
            distance_to_grid=feature_vector["distance_to_grid"],
            environmental_rating=feature_vector["environmental_rating"],
            economic_rating=feature_vector["economic_rating"],
        )