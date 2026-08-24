from backend.app.evaluation.ranking import (
    rank_candidate_sites,
    get_best_candidate_site
)


def test_sites_are_ranked_by_overall_score():

    sites = [
        {
            "site_id": "SITE-A",
            "overall_score": 71.06
        },
        {
            "site_id": "SITE-B",
            "overall_score": 88.50
        },
        {
            "site_id": "SITE-C",
            "overall_score": 62.40
        }
    ]

    ranked_sites = rank_candidate_sites(sites)

    print("\nRANKED CANDIDATE SITES")
    print("======================")

    for site in ranked_sites:
        print(
            f"Rank {site['rank']} | "
            f"{site['site_id']} | "
            f"Score: {site['overall_score']}"
        )

    assert ranked_sites[0]["site_id"] == "SITE-B"
    assert ranked_sites[1]["site_id"] == "SITE-A"
    assert ranked_sites[2]["site_id"] == "SITE-C"


def test_best_candidate_site():

    sites = [
        {
            "site_id": "SITE-A",
            "overall_score": 71.06
        },
        {
            "site_id": "SITE-B",
            "overall_score": 88.50
        },
        {
            "site_id": "SITE-C",
            "overall_score": 62.40
        }
    ]

    best_site = get_best_candidate_site(sites)

    print("\nBEST CANDIDATE SITE")
    print("===================")
    print(f"Site ID: {best_site['site_id']}")
    print(f"Score: {best_site['overall_score']}")

    assert best_site["site_id"] == "SITE-B"
    assert best_site["overall_score"] == 88.50