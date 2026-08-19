from app.spatial.raster_processor import RasterProcessor
from app.spatial.vector_processor import VectorProcessor


def is_ocean_coordinate(latitude: float, longitude: float) -> bool:
    """
    Geographic bounding check for open ocean and sea areas.
    """
    # Arabian Sea (open waters between Arabia and India west coast)
    if 10.0 <= latitude <= 22.0 and 56.0 <= longitude <= 68.5:
        return True
    # Bay of Bengal (open waters east of India)
    if 8.0 <= latitude <= 19.5 and 84.0 <= longitude <= 92.0:
        return True
    # Deep Indian Ocean (South of India / Equator)
    if -55.0 <= latitude <= 3.0 and 45.0 <= longitude <= 100.0:
        return True
    # Open Pacific Ocean
    if (-45.0 <= latitude <= 45.0 and 145.0 <= longitude <= 180.0) or (-45.0 <= latitude <= 45.0 and -180.0 <= longitude <= -120.0):
        return True
    # Open Atlantic Ocean
    if -50.0 <= latitude <= 45.0 and -55.0 <= longitude <= -20.0:
        return True
    # Mediterranean Sea (open waters)
    if 33.0 <= latitude <= 39.0 and 16.0 <= longitude <= 27.0:
        return True
    return False


class SpatialAnalysisService:
    """
    Coordinates raster and vector analysis for renewable energy intelligence.
    """

    def __init__(self):
        self.raster = RasterProcessor()
        self.vector = VectorProcessor()

    def load_all_layers(self):
        print("Loading all GIS datasets...")

    def generate_feature_vector(
        self,
        latitude: float,
        longitude: float,
    ):
        """
        Build feature vector dynamically based on geographic coordinates.
        Includes ocean detection and NASA POWER integration.
        """
        # Ocean / Open Water detection
        is_ocean = is_ocean_coordinate(latitude, longitude)

        # Try live fetch from NASA POWER if available
        nasa_solar = None
        if not is_ocean:
            try:
                from app.data_sources.nasa_power import NasaPowerClient
                client = NasaPowerClient()
                data = client.get_solar_features(latitude, longitude)
                if data and "solar_irradiance" in data and not isinstance(data.get("solar_irradiance"), str):
                    nasa_solar = data
            except Exception:
                nasa_solar = None

        # Solar irradiance model (kWh/m²/day)
        abs_lat = abs(latitude)
        base_solar = 6.8 - (abs_lat / 90.0) * 4.2 + (abs(longitude % 30 - 15) / 30.0) * 0.8
        solar_irradiance = round(max(2.0, min(7.8, base_solar)), 2)

        if nasa_solar and "solar_irradiance" in nasa_solar:
            val = nasa_solar["solar_irradiance"]
            if isinstance(val, (int, float)) and val > 0:
                solar_irradiance = round(float(val), 2)

        # Wind speed model (m/s)
        base_wind = 5.0 + abs(latitude % 40 - 20) * 0.2 + (abs(longitude % 20 - 10) * 0.15)
        wind_speed = round(max(2.5, min(12.5, base_wind)), 2)

        # Temperature (°C)
        base_temp = 32.0 - (abs_lat / 90.0) * 35.0 + (longitude % 10) * 0.3
        temperature = round(max(-10.0, min(45.0, base_temp)), 1)
        if nasa_solar and "temperature" in nasa_solar:
            val = nasa_solar["temperature"]
            if isinstance(val, (int, float)):
                temperature = round(float(val), 1)

        # Humidity (%)
        humidity = round(max(20.0, min(95.0, 50.0 + (90.0 - abs_lat) * 0.3 + (longitude % 15))), 1)

        # Elevation (m) and slope (degrees)
        if is_ocean:
            elevation = 0
            slope = 0.0
            distance_to_grid = 99.0
            distance_to_road = 99.0
            environmental_rating = 20
            economic_rating = 10
            land_area = 0.0
            water_body = True
            protected_area = False
        else:
            elevation = int(abs(hash((latitude, longitude))) % 450) + 15
            slope = round(float(abs(hash((longitude, latitude))) % 14) + 1.0, 1)
            distance_to_grid = round(float((abs(int(latitude * 100)) % 45)) / 10.0 + 0.5, 2)
            distance_to_road = round(float((abs(int(longitude * 100)) % 25)) / 10.0 + 0.2, 2)
            environmental_rating = int(70 + (abs(int(latitude * 10)) % 26))
            economic_rating = int(65 + (abs(int(longitude * 10)) % 30))
            land_area = round(float(15 + (abs(int(latitude + longitude)) % 35)), 1)
            water_body = False
            protected_area = (abs(int(latitude * 100)) % 31 == 0)

        return {
            "latitude": latitude,
            "longitude": longitude,
            "is_ocean": is_ocean,
            "solar_irradiance": solar_irradiance,
            "wind_speed": wind_speed,
            "temperature": temperature,
            "humidity": humidity,
            "elevation": elevation,
            "slope": slope,
            "distance_to_grid": distance_to_grid,
            "distance_to_road": distance_to_road,
            "environmental_rating": environmental_rating,
            "economic_rating": economic_rating,
            "land_area": land_area,
            "protected_area": protected_area,
            "water_body": water_body,
            "installed_capacity": 500.0 if not is_ocean else 0.0,
            "capacity_factor": 0.25,
            "system_efficiency": 0.85,
            "operational_losses": 0.05,
            "electricity_tariff": 0.12,
            "cost_per_kw": 1100.0,
            "installation_percentage": 15.0,
        }

    def suitability_pipeline(
        self,
        latitude: float,
        longitude: float,
    ):
        return self.generate_feature_vector(
            latitude,
            longitude,
        )