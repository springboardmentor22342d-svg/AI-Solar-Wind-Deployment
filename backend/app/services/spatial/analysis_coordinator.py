import logging
from typing import Dict, Any
from app.utils.coordinates import Coordinate, create_coordinate
from app.services.spatial.raster_processor import RasterProcessor
from app.services.spatial.vector_processor import VectorProcessor
from app.data_sources.nasa_power import NasaPowerClient, NasaPowerAPIError
from app.services.deployment_strategy import recommend_deployment

logger = logging.getLogger(__name__)

class SpatialAnalysisService:
    """
    Coordinates spatial analysis tasks by combining raster and vector processing,
    as well as external API calls (e.g., NASA POWER) and deployment strategies.
    """

    def __init__(self):
        # Initialize processors for various data layers
        self.solar_raster = RasterProcessor()
        self.wind_raster = RasterProcessor()
        self.slope_raster = RasterProcessor()
        self.grid_vector = VectorProcessor()
        self.road_vector = VectorProcessor()
        self.protected_areas_vector = VectorProcessor()
        self.water_bodies_vector = VectorProcessor()
        
        self.nasa_client = NasaPowerClient()

    def run_suitability_analysis(self, site_id: int, lat: float, lon: float) -> Dict[str, Any]:
        """
        Runs a comprehensive suitability analysis for a given location.
        
        Args:
            site_id: Identifier for the site.
            lat: Latitude of the site.
            lon: Longitude of the site.
            
        Returns:
            dict: Detailed evaluation report following the required format.
        """
        coord = create_coordinate(lat, lon)
        
        remarks = []
        
        # 1. Solar Irradiance (Real API with fallback)
        try:
            nasa_data = self.nasa_client.get_solar_irradiance(lat, lon)
            solar_val = nasa_data.get("solar_irradiance")
            if solar_val is None:
                raise ValueError("Missing solar irradiance in NASA data.")
        except Exception as e:
            logger.warning(f"Failed to fetch NASA data, simulating fallback: {e}")
            solar_val = round(3.5 + (abs(lat) % 4.0), 2)
            remarks.append("Solar irradiance simulated dynamically (NASA API fallback).")
            
        # 2. Wind Speed (Simulated dynamically)
        wind_val = round(4.0 + (abs(lat) / 10.0) + (abs(lon) % 5.0), 2)
        remarks.append("Wind speed simulated dynamically based on coordinates.")
        
        # 3. Spatial Features (Simulated dynamically)
        slope_val = round((abs(lat) + abs(lon)) % 15.0, 2)
        dist_grid = round((abs(lat) * abs(lon)) % 20.0, 2)
        dist_road = round((abs(lat) + abs(lon)) % 10.0, 2)
        remarks.append("Spatial features (slope, distance to grid/road) simulated dynamically.")
        
        # 4. Constraints (Simulated dynamically)
        is_protected = (int(abs(lat)) % 7 == 0)
        is_water = (int(abs(lon)) % 11 == 0)
        if is_protected or is_water:
            remarks.append("Spatial constraints simulated: Site overlaps with protected area or water body.")
        
        # 5. Deployment Strategy Integration
        deployment_recommendation = recommend_deployment(solar_val, wind_val)
        
        overall_score = deployment_recommendation["confidence"]
        
        # If site hits a hard constraint, reduce confidence score significantly
        if is_protected or is_water:
            overall_score = min(overall_score, 20)
            recommendation = "Not Recommended (Constraints)"
            remarks.append("Recommendation overridden due to spatial constraints.")
        else:
            recommendation = deployment_recommendation["deployment"]
            remarks.insert(0, deployment_recommendation["reason"])

        report = {
            "site_id": site_id,
            "latitude": lat,
            "longitude": lon,
            "overall_score": float(overall_score),
            "recommendation": recommendation,
            "criteria_evaluation": {
                "solar_irradiance": {
                    "value": solar_val,
                    "status": "Pass" if solar_val > 4.5 else "Fail"
                },
                "wind_speed": {
                    "value": wind_val,
                    "status": "Pass" if wind_val > 6.0 else "Fail"
                },
                "slope": {
                    "value": slope_val,
                    "status": "Pass" if slope_val < 10 else "Fail"
                },
                "distance_to_grid": {
                    "value": dist_grid,
                    "status": "Pass" if dist_grid < 10 else "Fail"
                },
                "distance_to_road": {
                    "value": dist_road,
                    "status": "Pass" if dist_road < 5 else "Fail"
                }
            },
            "constraints": {
                "protected_area": is_protected,
                "water_body": is_water
            },
            "remarks": remarks
        }
        
        return report
