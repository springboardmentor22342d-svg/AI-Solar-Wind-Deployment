"""
app/data_sources package.
Exposes dataset clients for external data integration.
"""

from .nasa_power import NasaPowerClient
from .global_wind_atlas import GlobalWindAtlasClient
from .srtm import SrtmClient
from .osm import OsmClient

__all__ = [
    "NasaPowerClient",
    "GlobalWindAtlasClient",
    "SrtmClient",
    "OsmClient",
]
