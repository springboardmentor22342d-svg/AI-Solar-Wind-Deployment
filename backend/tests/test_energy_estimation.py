"""
Tests for the Energy Estimation Service (Task 5)

NOTE: The estimation functions apply default system efficiencies:
  - Solar: 0.80 (80%)
  - Wind:  0.85 (85%)
All expected values below include these efficiency factors.
"""

import pytest
from app.services.energy_estimation import (
    estimate_solar_energy,
    estimate_wind_energy,
    estimate_annual_energy,
    HOURS_PER_YEAR
)

def test_estimate_solar_energy():
    """Test basic solar energy calculation."""
    # 10 MW at 20% CF, 80% efficiency = 10 * 0.20 * 8760 * 0.80 = 14016.0 MWh
    assert estimate_solar_energy(10.0, 20.0) == 14016.0

    # 0 capacity should yield 0
    assert estimate_solar_energy(0.0, 20.0) == 0.0

    # 0 CF should yield 0
    assert estimate_solar_energy(10.0, 0.0) == 0.0

def test_estimate_wind_energy():
    """Test basic wind energy calculation."""
    # 50 MW at 35% CF, 85% efficiency = 50 * 0.35 * 8760 * 0.85 = 130305.0 MWh
    assert estimate_wind_energy(50.0, 35.0) == 130305.0

def test_invalid_inputs_raise_errors():
    """Test that negative inputs raise ValueError."""
    with pytest.raises(ValueError):
        estimate_solar_energy(-10.0, 20.0)
    with pytest.raises(ValueError):
        estimate_wind_energy(10.0, -5.0)
    with pytest.raises(ValueError):
        estimate_annual_energy({}, "Solar", -100.0)

def test_higher_capacity_factor_increases_energy():
    """Higher capacity factors should produce higher annual energy."""
    energy_low = estimate_solar_energy(10.0, 15.0)
    energy_high = estimate_solar_energy(10.0, 25.0)
    assert energy_high > energy_low

def test_estimate_annual_energy_solar():
    """Test the service router for Solar deployment."""
    site_eval = {
        "solar_capacity_factor": 25.0,
        "wind_capacity_factor": 15.0
    }

    # 100 MW Solar at 25% CF, 80% eff = 100 * 0.25 * 8760 * 0.80 = 175200.0
    result = estimate_annual_energy(site_eval, "Solar", 100.0)

    assert result["solar_energy_mwh"] == 175200.0
    assert result["wind_energy_mwh"] == 0.0
    assert result["total_energy_mwh"] == 175200.0

def test_estimate_annual_energy_wind():
    """Test the service router for Wind deployment."""
    site_eval = {
        "solar_capacity_factor": 20.0,
        "wind_capacity_factor": 40.0
    }

    # 100 MW Wind at 40% CF, 85% eff = 100 * 0.40 * 8760 * 0.85 = 297840.0
    result = estimate_annual_energy(site_eval, "Wind", 100.0)

    assert result["solar_energy_mwh"] == 0.0
    assert result["wind_energy_mwh"] == 297840.0
    assert result["total_energy_mwh"] == 297840.0

def test_estimate_annual_energy_hybrid():
    """Test the service router for Hybrid deployment."""
    site_eval = {
        "solar_capacity_factor": 20.0,
        "wind_capacity_factor": 30.0
    }

    # 100 MW Hybrid with default 50/50 split
    # Solar: 50 MW at 20% CF, 80% eff = 50 * 0.20 * 8760 * 0.80 = 70080.0
    # Wind:  50 MW at 30% CF, 85% eff = 50 * 0.30 * 8760 * 0.85 = 111690.0
    # Total: 181770.0

    result = estimate_annual_energy(site_eval, "Hybrid", 100.0)

    assert result["solar_energy_mwh"] == 70080.0
    assert result["wind_energy_mwh"] == 111690.0
    assert result["total_energy_mwh"] == 181770.0

def test_hybrid_custom_split():
    """Test Hybrid deployment with a custom split ratio."""
    site_eval = {
        "solar_capacity_factor": 20.0,
        "wind_capacity_factor": 30.0
    }

    # 100 MW Hybrid with 80% Solar / 20% Wind
    # Solar: 80 MW at 20% CF, 80% eff = 80 * 0.20 * 8760 * 0.80 = 112128.0
    # Wind:  20 MW at 30% CF, 85% eff = 20 * 0.30 * 8760 * 0.85 = 44676.0
    # Total: 156804.0

    result = estimate_annual_energy(site_eval, "Hybrid", 100.0, hybrid_split_ratio=0.8)

    assert result["solar_energy_mwh"] == 112128.0
    assert result["wind_energy_mwh"] == 44676.0
    assert result["total_energy_mwh"] == 156804.0

def test_not_recommended_returns_zero():
    """Test that 'Not Recommended' returns 0."""
    site_eval = {
        "solar_capacity_factor": 10.0,
        "wind_capacity_factor": 10.0
    }

    result = estimate_annual_energy(site_eval, "Not Recommended", 100.0)

    assert result["solar_energy_mwh"] == 0.0
    assert result["wind_energy_mwh"] == 0.0
    assert result["total_energy_mwh"] == 0.0

def test_consistent_calculations():
    """The estimation logic remains consistent across different capacities."""
    site_eval = {"solar_capacity_factor": 20.0}

    # 50 MW should produce exactly half the energy of 100 MW
    res_100 = estimate_annual_energy(site_eval, "Solar", 100.0)
    res_50 = estimate_annual_energy(site_eval, "Solar", 50.0)

    assert res_50["total_energy_mwh"] * 2 == res_100["total_energy_mwh"]
