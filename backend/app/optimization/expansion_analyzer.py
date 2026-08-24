
class ExpansionAnalyzer:

    def analyze(self, site):
        land_area = site.get("land_area", 0)
        overall_score = site.get("overall_score", 0)

        if land_area >= 200 and overall_score >= 80:
            status = "Expandable"
            reason = "Sufficient land and high suitability for future expansion."

        elif land_area >= 100 and overall_score >= 60:
            status = "Limited Expansion"
            reason = "Moderate land availability allows limited future expansion."

        else:
            status = "Not Expandable"
            reason = "Insufficient land or low suitability for expansion."

        return {
            "expansion_status": status,
            "reason": reason
        }