from .planner import generate_plan
class  OptimizationEngine:
    def optimize(self,site):
        return generate_plan(site)