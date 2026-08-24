class HardConstraintValidator:
    """
    Validates mandatory technical constraints for a renewable energy site.
    """

    # Project thresholds
    MIN_SOLAR_IRRADIANCE = 4.0
    MIN_WIND_SPEED = 3.0
    MAX_SLOPE = 15.0
    MAX_GRID_DISTANCE = 20.0
    MAX_ROAD_DISTANCE = 10.0

    def validate(self, features):
        failed_constraints = []

        # 1. Solar irradiance
        if features["solar_irradiance"] < self.MIN_SOLAR_IRRADIANCE:
            failed_constraints.append(
                "Insufficient solar irradiance"
            )

        # 2. Wind speed
        if features["wind_speed"] < self.MIN_WIND_SPEED:
            failed_constraints.append(
                "Insufficient wind speed"
            )

        # 3. Terrain slope
        if features["slope"] > self.MAX_SLOPE:
            failed_constraints.append(
                "Unacceptable terrain slope"
            )

        # 4. Distance to electrical grid
        if features["distance_to_grid"] > self.MAX_GRID_DISTANCE:
            failed_constraints.append(
                "Site is too far from the electrical grid"
            )

        # 5. Distance to road
        if features["distance_to_road"] > self.MAX_ROAD_DISTANCE:
            failed_constraints.append(
                "Site is too far from a road"
            )

        feasible = len(failed_constraints) == 0

        return {
            "feasible": feasible,
            "failed_constraints": failed_constraints
        }