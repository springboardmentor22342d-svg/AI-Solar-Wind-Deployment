from app.services.solar_assessment import SolarAssessmentService
from app.services.wind_assessment import WindAssessmentService
from app.services.hybrid_recommendation import HybridRecommendationService


class DeploymentStrategyService:

    def __init__(self):
        self.solar_service = SolarAssessmentService()
        self.wind_service = WindAssessmentService()
        self.hybrid_service = HybridRecommendationService()

    def recommend_from_features(
        self,
        feature_vector: dict,
    ):
        """
        Generate deployment recommendation directly from a feature vector.
        """
        return self.recommend_deployment(
            solar_irradiance=feature_vector["solar_irradiance"],
            wind_speed=feature_vector["wind_speed"],
            is_ocean=feature_vector.get("is_ocean", False),
            water_body=feature_vector.get("water_body", False),
            resource_score=feature_vector.get("resource_score", 75.0),
        )

    def recommend_deployment(
        self,
        solar_irradiance: float,
        wind_speed: float,
        is_ocean: bool = False,
        water_body: bool = False,
        resource_score: float = 75.0,
    ):
        """
        Generate complete deployment recommendation with dynamic confidence.
        """
        if is_ocean or (water_body and resource_score < 40):
            return {
                "solar": {"solar_irradiance": solar_irradiance, "solar_class": "Unfeasible", "capacity_factor": 0},
                "wind": {"wind_speed": wind_speed, "wind_class": "Unfeasible", "capacity_factor": 0},
                "recommendation": "Unfeasible",
                "reason": "The selected location is situated in an ocean or open water body. Construction of land-based solar/wind power plants is not technically feasible.",
                "confidence_score": 0.0,
            }

        solar_result = self.solar_service.classify_solar_site(solar_irradiance)
        wind_result = self.wind_service.classify_wind_site(wind_speed)

        recommendation = self.hybrid_service.recommend(
            solar_result["solar_class"],
            wind_result["wind_class"],
        )

        conf_score = self.confidence_score(
            solar_irradiance,
            wind_speed,
            solar_result["solar_class"],
            wind_result["wind_class"],
            recommendation,
        )

        return {
            "solar": solar_result,
            "wind": wind_result,
            "recommendation": recommendation,
            "reason": self.generate_reason(
                recommendation,
                solar_result["solar_class"],
                wind_result["wind_class"],
                solar_irradiance,
                wind_speed,
            ),
            "confidence_score": conf_score,
        }

    def generate_reason(
        self,
        recommendation: str,
        solar_class: str = "Good",
        wind_class: str = "Moderate",
        solar_irradiance: float = 5.5,
        wind_speed: float = 6.0,
    ):
        """
        Return a clear human-readable technical reason for the recommendation.
        """
        if recommendation == "Solar":
            return (
                f"The site receives strong solar irradiance ({solar_irradiance} kWh/m²/day, classified as '{solar_class}'), "
                f"outperforming wind availability ({wind_speed} m/s). Solar PV installation is optimal."
            )

        elif recommendation == "Wind":
            return (
                f"The site has high average wind speeds ({wind_speed} m/s, classified as '{wind_class}'), "
                f"making wind turbine generators the most productive deployment choice."
            )

        elif recommendation == "Hybrid":
            return (
                f"Both solar irradiance ({solar_irradiance} kWh/m²/day, '{solar_class}') and wind speeds ({wind_speed} m/s, '{wind_class}') "
                f"are suitable and complementary, enabling a balanced hybrid solar-wind farm."
            )

        return "No clear recommendation available due to insufficient renewable resources."

    def confidence_score(
        self,
        solar_irradiance: float,
        wind_speed: float,
        solar_class: str,
        wind_class: str,
        recommendation: str,
    ) -> float:
        """
        Calculate dynamic continuous confidence score (0-100%) based on physical resource levels.
        """
        # Continuous solar score (0-100)
        solar_pct = min(100.0, max(10.0, (solar_irradiance / 6.5) * 100.0))
        
        # Continuous wind score (0-100)
        wind_pct = min(100.0, max(10.0, (wind_speed / 8.5) * 100.0))

        if recommendation == "Solar":
            raw_conf = solar_pct * 0.8 + wind_pct * 0.2
        elif recommendation == "Wind":
            raw_conf = wind_pct * 0.8 + solar_pct * 0.2
        elif recommendation == "Hybrid":
            # Hybrid benefits from combined strength
            raw_conf = (solar_pct + wind_pct) / 2.0 + 8.0
        else:
            raw_conf = 30.0

        final_conf = min(98.5, max(35.0, raw_conf))
        return round(final_conf, 1)