from app.services.overall_scoring import OverallScoringService

service = OverallScoringService()

test_cases = [
    {
        "name": "Excellent Site",
        "data": {
            "solar_irradiance": 8,
            "wind_speed": 12,
            "slope": 2,
            "elevation": 200,
            "distance_to_road": 0.5,
            "distance_to_grid": 1,
            "environmental_rating": 95,
            "economic_rating": 90,
        },
    },
    {
        "name": "Average Site",
        "data": {
            "solar_irradiance": 5,
            "wind_speed": 6,
            "slope": 10,
            "elevation": 1000,
            "distance_to_road": 4,
            "distance_to_grid": 6,
            "environmental_rating": 75,
            "economic_rating": 70,
        },
    },
    {
        "name": "Poor Site",
        "data": {
            "solar_irradiance": 2,
            "wind_speed": 3,
            "slope": 25,
            "elevation": 2500,
            "distance_to_road": 8,
            "distance_to_grid": 15,
            "environmental_rating": 50,
            "economic_rating": 45,
        },
    },
]

for case in test_cases:

    print("=" * 60)
    print(case["name"])
    print("=" * 60)

    result = service.calculate_overall_score(
        **case["data"]
    )

    for key, value in result.items():
        print(f"{key:25}: {value}")

    print()