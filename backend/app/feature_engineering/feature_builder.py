from app.services.dataset_services import DatasetServices
class featureBuilder:
    def __init__(self):
        self.dataset_service = DatasetServices()
        def build_features(self,latitude,longitude):
            solar = self.dataset_service.nasa.get_solar_data(latitude,longitude)
            wind = self.dataset_service.wind.get_wind_data(latitude,longitude)
            terrain = self.dataset_services.srtm.get_elevation(latitude,longitude)
            roads = self.dataset_services.osm.get_nearby_roads(latitude,longitude)
            pass
