from app.feasibility.hard_constraints import HardConstraintValidator
from app.feasibility.soft_constraints import SoftConstraintScorer


class FeasibilityEngine:

    def __init__(self):

        self.hard_validator = HardConstraintValidator()

        self.soft_scorer = SoftConstraintScorer()

    def evaluate(self, site):

        hard_result = self.hard_validator.validate(site)

        soft_result = self.soft_scorer.score(site)

        if hard_result["passed"]:

            if soft_result["score"] >= 80:
                recommendation = "Highly Feasible"

            elif soft_result["score"] >= 60:
                recommendation = "Moderately Feasible"

            else:
                recommendation = "Marginally Feasible"

        else:

            recommendation = "Not Technically Feasible"

        return {

            "technical_feasible": hard_result["passed"],

            "feasibility_score": soft_result["score"],

            "recommendation": recommendation,

            "constraint_summary": {

                "hard_constraints": hard_result,

                "soft_constraints": soft_result

            }

        }