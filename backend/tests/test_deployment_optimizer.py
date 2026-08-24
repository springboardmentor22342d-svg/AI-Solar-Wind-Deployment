import pytest

from backend.app.optimization.deployment_optimizer import DeploymentOptimizer


optimizer = DeploymentOptimizer()


def test_hybrid_deployment():
    site = {
        "solar_score": 90,
        "wind_score": 85,
        "overall_score": 88
    }

    result = optimizer.determine_strategy(site)

    assert result["deployment"] == "Hybrid"
    assert result["confidence"] == 93
    assert "reason" in result


def test_solar_deployment():
    site = {
        "solar_score": 85,
        "wind_score": 60,
        "overall_score": 75
    }

    result = optimizer.determine_strategy(site)

    assert result["deployment"] == "Solar"
    assert result["confidence"] == 85


def test_wind_deployment():
    site = {
        "solar_score": 60,
        "wind_score": 82,
        "overall_score": 74
    }

    result = optimizer.determine_strategy(site)

    assert result["deployment"] == "Wind"
    assert result["confidence"] == 82


def test_solar_preferred_when_scores_are_close():
    site = {
        "solar_score": 72,
        "wind_score": 68,
        "overall_score": 70
    }

    result = optimizer.determine_strategy(site)

    assert result["deployment"] == "Solar"


def test_wind_preferred_when_scores_are_close():
    site = {
        "solar_score": 65,
        "wind_score": 70,
        "overall_score": 68
    }

    result = optimizer.determine_strategy(site)

    assert result["deployment"] == "Wind"