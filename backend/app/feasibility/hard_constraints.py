class HardConstraintValidator:

    def validate(self, site):

        failures = []

        if site.get("is_ocean") or (site.get("elevation", 10) <= 0 and site.get("water_body")):
            failures.append("Site is located in an ocean or open water body; land-based solar/wind plant deployment is not technically feasible.")

        elif site.get("water_body"):
            failures.append("Site overlaps a water body.")

        if site.get("protected_area"):
            failures.append("Site lies inside an environmentally protected area.")

        if site.get("slope", 0) > 15:
            failures.append("Slope exceeds 15 degrees.")

        if site.get("land_area", 10) < 5:
            failures.append("Insufficient land area (minimum 5 acres required).")

        if site.get("environmental_rating", 70) < 50:
            failures.append("Environmental rating too low.")

        return {
            "passed": len(failures) == 0,
            "failures": failures
        }