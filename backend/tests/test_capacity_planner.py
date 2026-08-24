from backend.app.optimization.capacity_planner import CapacityPlanner

planner = CapacityPlanner()


def test_small_site():
    site = {
        "land_area": 15,
        "deployment": "Solar"
    }

    result = planner.estimate_capacity(site)

    assert result["recommended_capacity"] == 5


def test_medium_site():
    site = {
        "land_area": 60,
        "deployment": "Wind"
    }

    result = planner.estimate_capacity(site)

    assert result["recommended_capacity"] == 25


def test_large_site():
    site = {
        "land_area": 150,
        "deployment": "Hybrid"
    }

    result = planner.estimate_capacity(site)

    assert result["recommended_capacity"] == 50


def test_extra_large_site():
    site = {
        "land_area": 250,
        "deployment": "Solar"
    }

    result = planner.estimate_capacity(site)

    assert result["recommended_capacity"] == 100