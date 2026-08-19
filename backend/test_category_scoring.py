from app.services.category_scoring import CategoryScoringService

service = CategoryScoringService()

print(
    "Renewable Resource Score :",
    service.renewable_resource_score(
        solar_irradiance=7.2,
        wind_speed=9
    )
)

print(
    "Terrain Score :",
    service.terrain_score(
        slope=5,
        elevation=500
    )
)

print(
    "Infrastructure Score :",
    service.infrastructure_score(
        distance_to_road=1,
        distance_to_grid=2
    )
)

print(
    "Environmental Score :",
    service.environmental_score(88)
)

print(
    "Economic Score :",
    service.economic_score(79)
)