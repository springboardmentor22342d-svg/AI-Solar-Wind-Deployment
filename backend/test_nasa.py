from app.data_sources.nasa_power import NASAPowerClient
client = NASAPowerClient()
data = client.get_solar_data(
    latitude=20.2961,
    longitude=85.8245
)
print(client.extract_features(data))