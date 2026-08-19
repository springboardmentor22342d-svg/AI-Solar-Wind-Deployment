from app.services.deployment_optimizer import DeploymentOptimizer
from app.services.capacity_planner import CapacityPlanner
from app.services.expansion_analyzer import ExpansionAnalyzer


class DeploymentPlanService:
    """
    Generates a complete deployment plan
    by combining technology recommendation,
    capacity planning, and expansion analysis.
    """

    def __init__(self):
        self.optimizer = DeploymentOptimizer()
        self.capacity_planner = CapacityPlanner()
        self.expansion_analyzer = ExpansionAnalyzer()

    def generate_plan(
        self,
        deployment_type: str,
        solar_capacity_factor: float,
        wind_capacity_factor: float,
        land_area: float,
        resource_score: float,
    ):

        technology = {
            "recommended_technology": deployment_type
        }

        capacity = self.capacity_planner.recommend_capacity(
            land_area,
            resource_score,
        )

        expansion = self.expansion_analyzer.analyze(
            land_area,
            resource_score,
        )

        return {
            "recommended_technology":
                technology["recommended_technology"],

            "recommended_capacity_kw":
                capacity["recommended_capacity_kw"],

            "expansion_status":
                expansion["expansion_status"],

            "optimization_remarks":
                expansion["remarks"],
        }
    def generate_plan_from_features(
        self,
        feature_vector: dict,
    ):
        """
        Generate deployment plan
        directly from a feature vector.
        """

        return self.generate_plan(
            deployment_type=feature_vector["deployment"],
            solar_capacity_factor=feature_vector["solar_capacity_factor"],
            wind_capacity_factor=feature_vector["wind_capacity_factor"],
            land_area=feature_vector["land_area"],
            resource_score=feature_vector["resource_score"],
        )