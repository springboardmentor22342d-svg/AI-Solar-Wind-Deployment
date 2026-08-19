class HybridRecommendationService:

    def recommend(
        self,
        solar_class: str,
        wind_class: str,
    ):
        """
        Recommend the best deployment
        strategy based on solar and wind
        classifications.
        """

        if (
            solar_class == "Excellent"
            and wind_class == "Excellent"
        ):
            return "Hybrid"

        elif solar_class == "Excellent":
            return "Solar"

        elif wind_class == "Excellent":
            return "Wind"

        else:
            return "Hybrid"