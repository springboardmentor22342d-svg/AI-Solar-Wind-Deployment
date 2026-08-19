from app.services.overall_scoring import OverallScoringService

service = OverallScoringService()

result = service.calculate_overall_score(
    solar_irradiance=7.2,
    wind_speed=9,
    slope=5,
    elevation=500,
    distance_to_road=1,
    distance_to_grid=2,
    environmental_rating=88,
    economic_rating=79,
)

print(result)