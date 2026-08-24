from app.feasibility.hard_constraints import HardConstraints
from app.feasibility.soft_constraints import SoftConstraints

class FeasibilityEngine:
    def __init__(self):
        self.hard = HardConstraints()
        self.soft = SoftConstraints()
    def evaluate(self,feature):
        feasible,reasons = self.hard.validate(feature)
        score = self.soft.score(feature)
        return{
            "technical_feasible": feasible,
            "feasibility_score": score,
            "constraint_summary": reasons
        }