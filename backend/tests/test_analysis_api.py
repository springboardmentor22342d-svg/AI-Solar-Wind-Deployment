from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_analysis_api_success():

    response = client.post(
        "/analysis",
        json={
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "location" in data
    assert "solar" in data
    assert "wind" in data
    assert "site_suitability" in data
    assert "recommended_deployment" in data
    assert "technical_feasibility" in data
    assert "energy_yield" in data
    assert "financial_metrics" in data
    assert "recommendation_reason" in data


def test_analysis_api_location():

    response = client.post(
        "/analysis",
        json={
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["location"]["latitude"] == 17.3850
    assert data["location"]["longitude"] == 78.4867


def test_site_suitability():

    response = client.post(
        "/analysis",
        json={
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    )

    assert response.status_code == 200

    data = response.json()

    site_suitability = data["site_suitability"]

    assert "constraints_satisfied" in site_suitability
    assert "overall_score" in site_suitability
    assert "recommendation" in site_suitability
    assert "failed_constraints" in site_suitability


def test_technical_feasibility():

    response = client.post(
        "/analysis",
        json={
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    )

    assert response.status_code == 200

    data = response.json()

    feasibility = data["technical_feasibility"]

    assert "technically_feasible" in feasibility
    assert "hard_constraints" in feasibility
    assert "soft_score" in feasibility
    assert "decision" in feasibility


def test_energy_yield():

    response = client.post(
        "/analysis",
        json={
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    )

    assert response.status_code == 200

    data = response.json()

    energy = data["energy_yield"]

    assert "technology" in energy
    assert "total_annual_energy_mwh" in energy
    assert "total_annual_energy_gwh" in energy

    assert energy["total_annual_energy_mwh"] > 0
    assert energy["total_annual_energy_gwh"] > 0


def test_financial_metrics():

    response = client.post(
        "/analysis",
        json={
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    )

    assert response.status_code == 200

    data = response.json()

    financial = data["financial_metrics"]

    assert "annual_revenue" in financial
    assert "estimated_project_cost" in financial
    assert "payback_period" in financial
    assert "roi" in financial

    assert financial["annual_revenue"] >= 0
    assert financial["estimated_project_cost"] >= 0
    assert financial["roi"] >= 0


def test_recommendation():

    response = client.post(
        "/analysis",
        json={
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data["recommended_deployment"],
        str
    )

    assert isinstance(
        data["recommendation_reason"],
        str
    )

    assert len(
        data["recommendation_reason"]
    ) > 0


def test_invalid_latitude():

    response = client.post(
        "/analysis",
        json={
            "latitude": 120,
            "longitude": 78
        }
    )

    assert response.status_code == 422


def test_invalid_longitude():

    response = client.post(
        "/analysis",
        json={
            "latitude": 17,
            "longitude": 200
        }
    )

    assert response.status_code == 422


def test_missing_latitude():

    response = client.post(
        "/analysis",
        json={
            "longitude": 78
        }
    )

    assert response.status_code == 422


def test_missing_longitude():

    response = client.post(
        "/analysis",
        json={
            "latitude": 17
        }
    )

    assert response.status_code == 422


def test_multiple_locations():

    locations = [
        (17.3850, 78.4867),
        (13.0827, 80.2707),
        (19.0760, 72.8777)
    ]

    for latitude, longitude in locations:

        response = client.post(
            "/analysis",
            json={
                "latitude": latitude,
                "longitude": longitude
            }
        )

        assert response.status_code == 200

        data = response.json()

        assert "site_suitability" in data
        assert "solar" in data
        assert "wind" in data
        assert "recommended_deployment" in data
        assert "technical_feasibility" in data
        assert "energy_yield" in data
        assert "financial_metrics" in data
        assert "recommendation_reason" in data
