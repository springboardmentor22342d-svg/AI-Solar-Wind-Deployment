class ExpansionAnalyzer:
    """
    Determines whether a site has
    future expansion potential.
    """

    def analyze(
        self,
        land_area: float,
        resource_score: float,
    ):
        """
        Returns:
            Expandable
            Limited Expansion
            Not Expandable
        """

        if land_area >= 20 and resource_score >= 80:

            status = "Expandable"

            remarks = (
                "Excellent land availability and "
                "resource potential for future expansion."
            )

        elif land_area >= 10 and resource_score >= 50:

            status = "Limited Expansion"

            remarks = (
                "Moderate expansion potential. "
                "Expansion is possible with planning."
            )

        else:

            status = "Not Expandable"

            remarks = (
                "Limited land or poor resource "
                "availability."
            )

        return {
            "land_area_acres": land_area,
            "resource_score": resource_score,
            "expansion_status": status,
            "remarks": remarks,
        }