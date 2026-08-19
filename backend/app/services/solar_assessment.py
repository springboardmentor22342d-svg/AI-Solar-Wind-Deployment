class SolarAssessmentService:

    def calculate_solar_class(
        self,
        solar_irradiance: float,
    ):
        """
        Classify solar irradiance based
        on predefined ranges.
        """

        if solar_irradiance < 3:
            return "Poor"

        elif solar_irradiance < 5:
            return "Moderate"

        elif solar_irradiance < 7:
            return "Good"

        else:
            return "Excellent"

    def calculate_capacity_factor(
        self,
        solar_irradiance: float,
    ):
        """
        Estimate solar capacity factor
        based on solar irradiance.
        """

        if solar_irradiance < 3:
            return 15

        elif solar_irradiance < 5:
            return 30

        elif solar_irradiance < 7:
            return 45

        else:
            return 60

    def classify_solar_site(
        self,
        solar_irradiance: float,
    ):
        """
        Build a complete solar assessment.
        """

        solar_class = self.calculate_solar_class(
            solar_irradiance
        )

        capacity_factor = self.calculate_capacity_factor(
            solar_irradiance
        )

        return {
            "solar_irradiance": solar_irradiance,
            "solar_class": solar_class,
            "capacity_factor": capacity_factor,
        }