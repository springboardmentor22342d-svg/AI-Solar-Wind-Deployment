from app.services.site_ranking import SiteRankingService

service = SiteRankingService()

sites = [
    {
        "site_name": "Site A",
        "solar_irradiance": 7.2,
        "wind_speed": 9,
        "slope": 5,
        "elevation": 500,
        "distance_to_road": 1,
        "distance_to_grid": 2,
        "environmental_rating": 88,
        "economic_rating": 79,
    },
    {
        "site_name": "Site B",
        "solar_irradiance": 6.0,
        "wind_speed": 7,
        "slope": 8,
        "elevation": 800,
        "distance_to_road": 2,
        "distance_to_grid": 4,
        "environmental_rating": 80,
        "economic_rating": 75,
    },
    {
        "site_name": "Site C",
        "solar_irradiance": 7.8,
        "wind_speed": 10,
        "slope": 3,
        "elevation": 300,
        "distance_to_road": 0.5,
        "distance_to_grid": 1,
        "environmental_rating": 92,
        "economic_rating": 85,
    },
]

results = service.rank_sites(sites)

for index, site in enumerate(results, start=1):
    print(f"Rank {index}")
    print(site)
    print("-" * 50)