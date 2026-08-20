"""
Tests for the Site Suitability Scoring Engine (Task 5)
"""

import pytest
from app.services.site_scoring import (
    normalize_solar_irradiance,
    normalize_slope,
    normalize_distance,
    calculate_overall_score,
    rank_sites
)

def test_normalization_bounds():
    """Ensure normalization stays within 0-100 bounds."""
    assert normalize_solar_irradiance(-5.0) == 0.0
    assert normalize_solar_irradiance(16.0) == 100.0  # Max is 8.0, so 16.0 should be clamped to 100.0
    assert normalize_slope(40.0) == 0.0  # Max acceptable is 30
    assert normalize_distance(120.0, 100.0) == 0.0

def test_higher_renewable_resource_increases_score():
    """Higher renewable resource availability should increase the overall score."""
    base_site = {
        "slope_deg": 5.0,
        "dist_grid_km": 10.0,
        "dist_road_km": 5.0,
        "ndvi": 0.1,  # Barren, good for renewables
        "solar_irradiance_kwh": 3.0,
        "wind_speed_ms": 4.0
    }
    
    better_site = base_site.copy()
    better_site["solar_irradiance_kwh"] = 7.0
    better_site["wind_speed_ms"] = 8.0
    
    base_scores = calculate_overall_score(base_site)
    better_scores = calculate_overall_score(better_site)
    
    assert better_scores["renewable_score"] > base_scores["renewable_score"]
    assert better_scores["overall_score"] > base_scores["overall_score"]

def test_poor_infrastructure_reduces_score():
    """Poor infrastructure or terrain appropriately reduces the score."""
    good_site = {
        "solar_irradiance_kwh": 6.0,
        "wind_speed_ms": 7.0,
        "slope_deg": 2.0,
        "dist_grid_km": 5.0,
        "dist_road_km": 2.0
    }
    
    poor_infra_site = good_site.copy()
    poor_infra_site["dist_grid_km"] = 90.0  # Very far from grid
    poor_infra_site["dist_road_km"] = 45.0  # Very far from road
    poor_infra_site["slope_deg"] = 28.0     # Very steep
    
    good_scores = calculate_overall_score(good_site)
    poor_scores = calculate_overall_score(poor_infra_site)
    
    assert poor_scores["infrastructure_score"] < good_scores["infrastructure_score"]
    assert poor_scores["terrain_score"] < good_scores["terrain_score"]
    assert poor_scores["economic_score"] < good_scores["economic_score"]
    assert poor_scores["overall_score"] < good_scores["overall_score"]

def test_ranking_changes_correctly():
    """The ranking changes correctly when site parameters change."""
    site_a = {
        "id": "A",
        "solar_irradiance_kwh": 7.0,
        "wind_speed_ms": 8.0,
        "slope_deg": 5.0,
        "dist_grid_km": 10.0,
        "dist_road_km": 5.0
    }
    
    site_b = {
        "id": "B",
        "solar_irradiance_kwh": 4.0,
        "wind_speed_ms": 5.0,
        "slope_deg": 15.0,
        "dist_grid_km": 40.0,
        "dist_road_km": 20.0
    }
    
    # A has better stats across the board
    ranked = rank_sites([site_b, site_a])
    assert ranked[0]["id"] == "A"
    assert ranked[1]["id"] == "B"
    
    # Now make B significantly better than A
    site_b_improved = site_b.copy()
    site_b_improved["solar_irradiance_kwh"] = 8.0
    site_b_improved["wind_speed_ms"] = 10.0
    site_b_improved["slope_deg"] = 1.0
    site_b_improved["dist_grid_km"] = 2.0
    site_b_improved["dist_road_km"] = 1.0
    
    ranked_improved = rank_sites([site_a, site_b_improved])
    assert ranked_improved[0]["id"] == "B"
    assert ranked_improved[1]["id"] == "A"

def test_consistent_results():
    """The scoring logic produces consistent results for repeated evaluations."""
    site = {
        "solar_irradiance_kwh": 5.5,
        "wind_speed_ms": 6.5,
        "slope_deg": 10.0,
        "dist_grid_km": 25.0,
        "dist_road_km": 15.0,
        "ndvi": 0.2
    }
    
    eval1 = calculate_overall_score(site)
    eval2 = calculate_overall_score(site)
    eval3 = calculate_overall_score(site)
    
    assert eval1 == eval2
    assert eval2 == eval3
