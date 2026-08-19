from app.services.nasa_historical_service import NASAHistoricalService


service = NASAHistoricalService()

path = service.create_dataset(

    latitude=17.385,

    longitude=78.4867,

    start_date="20220101",

    end_date="20241231",

    filename="solar_history.csv",

)

print(path)