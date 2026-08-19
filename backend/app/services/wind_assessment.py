class WindAssessmentService:

    def calculate_wind_class(
        self,
        wind_speed: float,
    ):
        """
        Classify wind speed based on
        predefined ranges.
        """

        if wind_speed < 3:
            return "Poor"

        elif wind_speed < 5:
            return "Moderate"

        elif wind_speed < 7:
            return "Good"

        else:
            return "Excellent"

    def calculate_capacity_factor(
        self,
        wind_speed: float,
    ):
        """
        Estimate wind capacity factor
        based on wind speed.
        """

        if wind_speed < 3:
            return 10

        elif wind_speed < 5:
            return 25

        elif wind_speed < 7:
            return 40

        else:
            return 55

    def classify_wind_site(
        self,
        wind_speed: float,
    ):
        """
        Build a complete wind assessment.
        """

        wind_class = self.calculate_wind_class(
            wind_speed
        )

        capacity_factor = self.calculate_capacity_factor(
            wind_speed
        )

        return {
            "wind_speed": wind_speed,
            "wind_class": wind_class,
            "capacity_factor": capacity_factor,
        }