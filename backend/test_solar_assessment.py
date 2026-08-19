from app.services.solar_assessment import SolarAssessmentService

service = SolarAssessmentService()

test_values = [2.5, 4.2, 6.1, 7.8]

for irradiance in test_values:

    result = service.classify_solar_site(irradiance)

    print(result)