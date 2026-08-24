from typing import List, Dict


def rank_candidate_sites(
    site_results: List[Dict]
) -> List[Dict]:
    """
    Rank candidate sites based on overall site score.

    Highest score appears first.
    """

    ranked_sites = sorted(
        site_results,
        key=lambda site: site["overall_score"],
        reverse=True
    )

    for rank, site in enumerate(ranked_sites, start=1):
        site["rank"] = rank

    return ranked_sites


def get_best_candidate_site(
    site_results: List[Dict]
) -> Dict:
    """
    Return the most suitable candidate site.
    """

    if not site_results:
        raise ValueError(
            "At least one site result is required"
        )

    return max(
        site_results,
        key=lambda site: site["overall_score"]
    )