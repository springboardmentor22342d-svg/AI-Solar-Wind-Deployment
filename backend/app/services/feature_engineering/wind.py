from backend.app.data_sources.global_wind_atlas import GlobalWindAtlasClient

class WindService:

    def __init__(self):
        self.wind_client = GlobalWindAtlasClient()

    def get_wind_data(self, latitude: float, longitude: float):
        return self.wind_client.fetch(latitude, longitude)