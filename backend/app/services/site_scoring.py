"""
app/services/site_scoring.py – Site Suitability Scoring Engine

Provides reusable, independent functions to normalize inputs, compute
category-specific scores, and determine an overall site ranking.
"""

import math
from typing import Any, Dict, List, Optional

# Default weights for the overall site suitability score
DEFAULT_WEIGHTS = {
    "renewable_score": 0.40,
    "economic_score": 0.20,
    "terrain_score": 0.15,
    "infrastructure_score": 0.15,
    "environmental_score": 0.10,
}

# Maximum bounds used for normalization
MAX_SOLAR_KWH = 8.0     # Typical max annual average kWh/m2/day
MAX_WIND_MS = 12.0      # Typical max annual average m/s for onshore
MAX_SLOPE_DEG = 30.0    # Slopes > 30 deg are generally unsuitable
MAX_DIST_GRID_KM = 100.0
MAX_DIST_ROAD_KM = 50.0


def normalize_solar_irradiance(solar_kwh: float) -> float:
    """Normalize solar irradiance to a 0–100 scale (higher is better)."""
    if solar_kwh is None or solar_kwh < 0:
        return 0.0
    return min(100.0, (solar_kwh / MAX_SOLAR_KWH) * 100.0)

def normalize_wind_speed(wind_ms: float) -> float:
    """Normalize wind speed to a 0–100 scale (higher is better)."""
    if wind_ms is None or wind_ms < 0:
        return 0.0
    return min(100.0, (wind_ms / MAX_WIND_MS) * 100.0)

def normalize_slope(slope_deg: float) -> float:
    """Normalize terrain slope to a 0–100 scale (lower is better)."""
    if slope_deg is None or slope_deg < 0:
        return 0.0
    if slope_deg >= MAX_SLOPE_DEG:
        return 0.0
    return 100.0 - ((slope_deg / MAX_SLOPE_DEG) * 100.0)

def normalize_distance(dist_km: float, max_acceptable_km: float) -> float:
    """Normalize distance to a 0–100 scale (lower is better)."""
    if dist_km is None or dist_km < 0:
        return 0.0
    if dist_km >= max_acceptable_km:
        return 0.0
    return 100.0 - ((dist_km / max_acceptable_km) * 100.0)



def calculate_renewable_score(solar_kwh: float, wind_ms: float) -> float:
    """Calculate the Renewable Resource Score based on solar and wind potential."""
    solar_score = normalize_solar_irradiance(solar_kwh)
    wind_score = normalize_wind_speed(wind_ms)
    # Simple average, but ensures that even a single strong resource gives a good score
    return (solar_score + wind_score) / 2.0

def calculate_terrain_score(slope_deg: float, elevation_m: float) -> float:
    """Calculate the Terrain Score based on slope and elevation."""
    slope_score = normalize_slope(slope_deg)
    
    # Elevation penalty (arbitrary logic: deduct slightly for very high altitudes > 2000m)
    elevation_penalty = 0.0
    if elevation_m and elevation_m > 2000.0:
        # Deduct up to 20 points for extreme elevations up to 5000m
        excess_elevation = min(3000.0, elevation_m - 2000.0)
        elevation_penalty = (excess_elevation / 3000.0) * 20.0
        
    return max(0.0, slope_score - elevation_penalty)

def calculate_infrastructure_score(dist_grid_km: float, dist_road_km: float) -> float:
    """Calculate the Infrastructure Score based on proximity to grid and roads."""
    grid_score = normalize_distance(dist_grid_km, MAX_DIST_GRID_KM)
    road_score = normalize_distance(dist_road_km, MAX_DIST_ROAD_KM)
    # Grid access is slightly more important than road access
    return (grid_score * 0.6) + (road_score * 0.4)

def calculate_environmental_score(ndvi: Optional[float] = None, land_cover_class: Optional[str] = None) -> float:
    """
    Calculate the Environmental Score.
    Lower NDVI (barren land) is typically better to avoid ecological disruption.
    """
    score = 50.0  # Default neutral score
    if ndvi is not None:
        # Assuming NDVI ranges from -1 to 1. 
        # For utility-scale renewables, barren land (NDVI ~0 to 0.2) is ideal.
        # Dense vegetation (NDVI > 0.6) is penalized to avoid deforestation.
        if ndvi > 0.6:
            score = 20.0
        elif ndvi > 0.3:
            score = 60.0
        elif ndvi >= 0.0:
            score = 90.0
        else: # Water or snow (negative NDVI)
            score = 10.0
            
    if land_cover_class:
        lower_lc = land_cover_class.lower()
        if "forest" in lower_lc or "water" in lower_lc or "wetland" in lower_lc:
            score = min(score, 20.0) # Cap at 20 for protected/unsuitable areas
        elif "barren" in lower_lc or "desert" in lower_lc or "scrub" in lower_lc:
            score = max(score, 80.0) # Boost for barren areas
            
    return score

def calculate_economic_score(infrastructure_score: float, terrain_score: float) -> float:
    """
    Calculate the Economic Score.
    This is a derived score. Poor infrastructure and steep terrain significantly
    drive up capital expenditures (CAPEX).
    """
    # Both are crucial, if either is very low, it drags down the economic viability
    return (infrastructure_score * 0.5) + (terrain_score * 0.5)



def calculate_overall_score(site_data: Dict[str, Any], weights: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
    """
    Combine all category scores into a single Overall Site Suitability Score.
    
    Args:
        site_data: Dictionary containing input parameters (solar_irradiance_kwh, wind_speed_ms, etc.)
        weights: Dictionary of custom weights. Uses DEFAULT_WEIGHTS if None.
        
    Returns:
        A dictionary with individual category scores and the `overall_score`.
    """
    w = weights or DEFAULT_WEIGHTS
    
    # Calculate categories
    renewable_score = calculate_renewable_score(
        site_data.get("solar_irradiance_kwh", 0), 
        site_data.get("wind_speed_ms", 0)
    )
    
    terrain_score = calculate_terrain_score(
        site_data.get("slope_deg", 0), 
        site_data.get("elevation_m", 0)
    )
    
    infrastructure_score = calculate_infrastructure_score(
        site_data.get("dist_grid_km", MAX_DIST_GRID_KM), 
        site_data.get("dist_road_km", MAX_DIST_ROAD_KM)
    )
    
    environmental_score = calculate_environmental_score(
        site_data.get("ndvi"), 
        site_data.get("land_cover_class")
    )
    
    economic_score = calculate_economic_score(
        infrastructure_score, 
        terrain_score
    )
    
    # Calculate overall weighted score
    overall_score = (
        (renewable_score * w.get("renewable_score", 0)) +
        (terrain_score * w.get("terrain_score", 0)) +
        (infrastructure_score * w.get("infrastructure_score", 0)) +
        (environmental_score * w.get("environmental_score", 0)) +
        (economic_score * w.get("economic_score", 0))
    )
    
    # Normalize overall score just in case weights sum > 1
    total_weight = sum(w.values())
    if total_weight > 0:
        overall_score = overall_score / total_weight
        
    return {
        "renewable_score": round(renewable_score, 2),
        "terrain_score": round(terrain_score, 2),
        "infrastructure_score": round(infrastructure_score, 2),
        "environmental_score": round(environmental_score, 2),
        "economic_score": round(economic_score, 2),
        "overall_score": round(overall_score, 2)
    }



def rank_sites(sites: List[Dict[str, Any]], weights: Optional[Dict[str, float]] = None) -> List[Dict[str, Any]]:
    """
    Accept multiple site evaluation results and rank them based on the 
    Overall Site Suitability Score in descending order.
    """
    evaluated_sites = []
    
    for site in sites:
        # Calculate scores for this site
        scores = calculate_overall_score(site, weights)
        
        # Merge the original site data with the calculated scores
        evaluated_site = site.copy()
        evaluated_site.update(scores)
        
        evaluated_sites.append(evaluated_site)
        
    # Sort by overall_score descending
    evaluated_sites.sort(key=lambda x: x["overall_score"], reverse=True)
    
    return evaluated_sites
