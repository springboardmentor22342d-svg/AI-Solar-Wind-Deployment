from app.data_sources.nasa_power import NasaPowerClient

client = NasaPowerClient()

data = client.get_solar_features(
    latitude=20.2961,
    longitude=85.8245
)

print(data)