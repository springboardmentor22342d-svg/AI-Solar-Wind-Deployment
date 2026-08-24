from app.data_sources.nasa_power import NASAPowerClient
from app.data_sources.global_wind_atlas import GlobalWindAtlasClient
from app.data_sources.srtm import SRTMClient
from app.data_sources.osm import OSMClient
class DatasetService:
    def __init__(self):
        self.nasa = NASAPowerClient()
        self.wind = GlobalWindAtlasClient()
        self.srtm = SRTMClient()
        self.osm = OSMClient()