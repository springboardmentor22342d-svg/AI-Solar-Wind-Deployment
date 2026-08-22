"""
Ranks multiple candidate sites by their Overall Site Suitability Score.
"""

from app.scoring.site_scorer import calculate_site_score


def rank_sites(sites: list[dict]) -> list[dict]:
    """
    Input: list of site dicts, each containing at least 'name' (or
    identifying info) plus the raw features needed for scoring.

    Output: the same sites, each annotated with their score
    breakdown, sorted by overall_score descending (best site first).
    """
    scored_sites = []
    for site in sites:
        scores = calculate_site_score(site)
        scored_sites.append({**site, **scores})

    return sorted(scored_sites, key=lambda s: s["overall_score"], reverse=True)


def explain_ranking(site_a: dict, site_b: dict) -> str:
    """
    Explains why one site outranks another, by comparing category
    scores and identifying the largest contributing differences.
    """
    scores_a = calculate_site_score(site_a)
    scores_b = calculate_site_score(site_b)

    diffs = {
        "resource_score": scores_a["resource_score"] - scores_b["resource_score"],
        "terrain_score": scores_a["terrain_score"] - scores_b["terrain_score"],
        "infrastructure_score": scores_a["infrastructure_score"] - scores_b["infrastructure_score"],
        "environmental_score": scores_a["environmental_score"] - scores_b["environmental_score"],
        "economic_score": scores_a["economic_score"] - scores_b["economic_score"],
    }

    biggest_factor = max(diffs, key=lambda k: abs(diffs[k]))
    direction = "higher" if diffs[biggest_factor] > 0 else "lower"
    winner = site_a.get("name", "Site A") if scores_a["overall_score"] > scores_b["overall_score"] else site_b.get("name", "Site B")

    return (
        f"{winner} scores {abs(scores_a['overall_score'] - scores_b['overall_score']):.2f} "
        f"points higher overall, primarily due to {direction} {biggest_factor.replace('_', ' ')} "
        f"({abs(diffs[biggest_factor]):.2f} point difference)."
    )