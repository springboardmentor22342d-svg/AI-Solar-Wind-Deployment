from app.services.capacity_planner import CapacityPlanner

planner = CapacityPlanner()

sites = [

    {
        "name": "Site A",
        "land": 20,
        "score": 92,
    },

    {
        "name": "Site B",
        "land": 15,
        "score": 70,
    },

    {
        "name": "Site C",
        "land": 10,
        "score": 45,
    }

]

for site in sites:

    print("=" * 60)

    print(site["name"])

    result = planner.recommend_capacity(
        land_area=site["land"],
        resource_score=site["score"],
    )

    print(result)