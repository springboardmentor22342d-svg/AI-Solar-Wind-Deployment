from backend.app.data_sources.nasa_power import NasaPowerClient


client = NasaPowerClient()

hyderabad = client.fetch(
    17.3850,
    78.4867
)

delhi = client.fetch(
    28.6139,
    77.2090
)

print("Hyderabad:")
print(hyderabad)

print("\nDelhi:")
print(delhi)