from app.services.overall_scoring import OverallScoringService


class SiteRankingService:

    def __init__(self):
        self.overall_service = OverallScoringService()

    def rank_sites(
        self,
        sites: list,
    ):

        ranked_sites = []

        for site in sites:

            score = self.overall_service.calculate_overall_score(
                solar_irradiance=site["solar_irradiance"],
                wind_speed=site["wind_speed"],
                slope=site["slope"],
                elevation=site["elevation"],
                distance_to_road=site["distance_to_road"],
                distance_to_grid=site["distance_to_grid"],
                environmental_rating=site["environmental_rating"],
                economic_rating=site["economic_rating"],
            )

            ranked_sites.append(
                {
                    "site_name": site["site_name"],
                    **score,
                }
            )

        ranked_sites.sort(
            key=lambda x: x["overall_score"],
            reverse=True,
        )

        return ranked_sites