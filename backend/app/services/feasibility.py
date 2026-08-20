"""
app/services/feasibility.py – Technical Feasibility Engine

Provides logic for evaluating hard constraints (mandatory requirements)
and scoring soft constraints (non-mandatory factors) to determine if a
renewable energy site is technically feasible.
"""
from typing import Dict, Any, Tuple

# Hard Constraints Thresholds
MAX_SLOPE_DEG = 15.0  # Sites with slope > 15 degrees are strictly rejected
MIN_ELEVATION_M = -50.0 # Extreme below sea level might be rejected (arbitrary example if needed)
MAX_ELEVATION_M = 4000.0 # Extreme altitudes rejected

# Soft Constraint Thresholds for Scoring
MAX_DIST_GRID_KM = 50.0
MAX_DIST_ROAD_KM = 25.0

def evaluate_hard_constraints(features: Dict[str, Any]) -> Tuple[bool, list]:
    """
    Evaluates mandatory constraints.
    Returns a tuple: (is_feasible, list_of_failed_constraints)
    """
    failed_constraints = []
    
    slope = features.get("slope_deg", 0.0)
    if slope > MAX_SLOPE_DEG:
        failed_constraints.append(f"Slope exceeds maximum allowed ({slope} > {MAX_SLOPE_DEG})")
        
    elevation = features.get("elevation_m", 0.0)
    if elevation and (elevation < MIN_ELEVATION_M or elevation > MAX_ELEVATION_M):
        failed_constraints.append(f"Elevation is out of bounds ({elevation})")
        
    # We can assume land_cover_class is a hard constraint if it's "urban" or "water"
    land_cover = features.get("land_cover_class", "").lower()
    if land_cover in ["water", "urban", "wetland"]:
        failed_constraints.append(f"Restricted land use ({land_cover})")

    is_feasible = len(failed_constraints) == 0
    return is_feasible, failed_constraints

def score_soft_constraints(features: Dict[str, Any]) -> float:
    """
    Calculates a feasibility score based on non-mandatory constraints
    like proximity to infrastructure.
    Returns a score between 0 and 100.
    """
    dist_grid = features.get("dist_grid_km", MAX_DIST_GRID_KM)
    dist_road = features.get("dist_road_km", MAX_DIST_ROAD_KM)
    
    # Normalize distances (0 to 100, where 0 distance = 100 score)
    grid_score = max(0.0, 100.0 * (1.0 - (dist_grid / MAX_DIST_GRID_KM))) if dist_grid <= MAX_DIST_GRID_KM else 0.0
    road_score = max(0.0, 100.0 * (1.0 - (dist_road / MAX_DIST_ROAD_KM))) if dist_road <= MAX_DIST_ROAD_KM else 0.0
    
    # We can weight grid proximity higher
    final_score = (grid_score * 0.7) + (road_score * 0.3)
    return round(final_score, 2)

def evaluate_feasibility(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main entry point for the Feasibility Module.
    Validates hard constraints and calculates soft constraint scores.
    """
    is_feasible, failed_constraints = evaluate_hard_constraints(features)
    soft_score = score_soft_constraints(features)
    
    # If not feasible, we might zero out or severely penalize the soft score,
    # but returning it as-is is fine for transparency, the 'is_feasible' flag is the hard gate.
    
    return {
        "is_feasible": is_feasible,
        "feasibility_score": soft_score,
        "failed_hard_constraints": failed_constraints,
        "constraint_summary": "Passed all hard constraints." if is_feasible else f"Failed {len(failed_constraints)} hard constraints."
    }
