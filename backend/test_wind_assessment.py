from app.services.wind_assessment import WindAssessmentService

service = WindAssessmentService()

test_values = [2.5, 4.0, 6.2, 8.5]

for speed in test_values:

    result = service.classify_wind_site(speed)

    print(result)