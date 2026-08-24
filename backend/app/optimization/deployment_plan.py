from backend.app.optimization.deployment_optimizer import DeploymentOptimizer
from backend.app.optimization.capacity_planner import CapacityPlanner
from backend.app.optimization.expansion_analyzer import ExpansionAnalyzer


class DeploymentPlanGenerator:

    def __init__(self):
        self.optimizer = DeploymentOptimizer()
        self.capacity_planner = CapacityPlanner()
        self.expansion_analyzer = ExpansionAnalyzer()

    def generate_plan(self, site):

        deployment = self.optimizer.determine_strategy(site)

        # Pass the selected technology to the capacity planner
        site["deployment"] = deployment["deployment"]

        capacity = self.capacity_planner.estimate_capacity(site)

        expansion = self.expansion_analyzer.analyze(site)

        remarks = (
            f"{deployment['reason']} "
            f"Recommended capacity: {capacity['recommended_capacity']} MW. "
            f"Expansion status: {expansion['expansion_status']}."
        )

        return {
            "recommended_technology": deployment["deployment"],
            "recommended_capacity": f"{capacity['recommended_capacity']} MW",
            "expansion_status": expansion["expansion_status"],
            "optimization_remarks": remarks
        }
    