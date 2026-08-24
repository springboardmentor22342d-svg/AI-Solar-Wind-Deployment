from backend.app.services.feature_engineering.solar import SolarService


solar_service = SolarService()

data = solar_service.get_solar_data(
    latitude=latitude ,
    longitude=longitude
)

print(data)