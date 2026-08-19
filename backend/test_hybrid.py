from app.services.hybrid_recommendation import HybridRecommendationService

service = HybridRecommendationService()

tests = [
    ("Excellent", "Poor"),
    ("Poor", "Excellent"),
    ("Excellent", "Excellent"),
    ("Good", "Moderate"),
]

for solar, wind in tests:
    result = service.recommend(solar, wind)

    print(
        f"Solar: {solar:10} Wind: {wind:10} -> {result}"
    )