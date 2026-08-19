from app.services.feature_engineering.solar import SolarFeatureEngineering

solar = SolarFeatureEngineering()

result = solar.build_features(
    latitude=20.2961,
    longitude=85.8245,
)

print(result)