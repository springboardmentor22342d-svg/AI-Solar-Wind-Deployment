from app.services.expansion_analyzer import ExpansionAnalyzer

analyzer = ExpansionAnalyzer()

sites = [

    {
        "name": "Site A",
        "land": 25,
        "score": 92,
    },

    {
        "name": "Site B",
        "land": 15,
        "score": 68,
    },

    {
        "name": "Site C",
        "land": 8,
        "score": 40,
    },

]

for site in sites:

    print("=" * 60)

    print(site["name"])

    result = analyzer.analyze(
        land_area=site["land"],
        resource_score=site["score"],
    )

    print(result)