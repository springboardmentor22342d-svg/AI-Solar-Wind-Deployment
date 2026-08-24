
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


# ============================================================
# TASK 3 — FINAL END-TO-END TESTING
# ============================================================


def validate_standard_response(data, location):
    """
    Validate the standardized final API response.
    """

    # --------------------------------------------------------
    # 1. Location
    # --------------------------------------------------------

    assert "location" in data

    assert data["location"]["latitude"] == location["latitude"]
    assert data["location"]["longitude"] == location["longitude"]

    # --------------------------------------------------------
    # 2. Required standardized response fields
    # --------------------------------------------------------

    required_fields = {
        "location",
        "site_suitability",
        "recommended_deployment",
        "technical_feasibility",
        "energy_yield",
        "financial_metrics",
        "recommendation_reason",
    }

    assert required_fields.issubset(data.keys())

    # --------------------------------------------------------
    # 3. Site Suitability
    # --------------------------------------------------------

    site_suitability = data["site_suitability"]

    assert isinstance(site_suitability, dict)

    assert "constraints_satisfied" in site_suitability
    assert "overall_score" in site_suitability
    assert "recommendation" in site_suitability
    assert "failed_constraints" in site_suitability

    assert isinstance(
        site_suitability["constraints_satisfied"],
        bool
    )

    assert isinstance(
        site_suitability["overall_score"],
        (int, float)
    )

    assert isinstance(
        site_suitability["recommendation"],
        str
    )

    assert isinstance(
        site_suitability["failed_constraints"],
        list
    )

    # --------------------------------------------------------
    # 4. Recommended Deployment
    # --------------------------------------------------------

    deployment = data["recommended_deployment"]

    assert isinstance(deployment, str)
    assert len(deployment) > 0

    # --------------------------------------------------------
    # 5. Technical Feasibility
    # --------------------------------------------------------

    technical = data["technical_feasibility"]

    assert isinstance(technical, dict)

    assert "technically_feasible" in technical
    assert "hard_constraints" in technical
    assert "soft_score" in technical
    assert "decision" in technical

    assert isinstance(
        technical["technically_feasible"],
        bool
    )

    assert isinstance(
        technical["hard_constraints"],
        dict
    )

    assert isinstance(
        technical["soft_score"],
        (int, float)
    )

    assert isinstance(
        technical["decision"],
        str
    )

    # --------------------------------------------------------
    # 6. Energy Yield
    # --------------------------------------------------------

    energy = data["energy_yield"]

    assert isinstance(energy, dict)

    assert "technology" in energy
    assert "total_annual_energy_mwh" in energy
    assert "total_annual_energy_gwh" in energy

    assert isinstance(
        energy["technology"],
        str
    )

    assert isinstance(
        energy["total_annual_energy_mwh"],
        (int, float)
    )

    assert isinstance(
        energy["total_annual_energy_gwh"],
        (int, float)
    )

    assert energy["total_annual_energy_mwh"] > 0
    assert energy["total_annual_energy_gwh"] > 0

    # --------------------------------------------------------
    # 7. Financial Metrics
    # --------------------------------------------------------

    financial = data["financial_metrics"]

    assert isinstance(financial, dict)

    assert "annual_revenue" in financial
    assert "estimated_project_cost" in financial
    assert "payback_period" in financial
    assert "roi" in financial

    assert isinstance(
        financial["annual_revenue"],
        (int, float)
    )

    assert isinstance(
        financial["estimated_project_cost"],
        (int, float)
    )

    assert isinstance(
        financial["payback_period"],
        (int, float)
    )

    assert isinstance(
        financial["roi"],
        (int, float)
    )

    assert financial["annual_revenue"] >= 0
    assert financial["estimated_project_cost"] >= 0
    assert financial["payback_period"] >= 0

    # --------------------------------------------------------
    # 8. Recommendation Reason
    # --------------------------------------------------------

    reason = data["recommendation_reason"]

    assert isinstance(reason, str)
    assert len(reason) > 0


# ============================================================
# TEST 1 — FIVE DIFFERENT VALID LOCATIONS
# ============================================================


def test_final_five_locations():
    """
    Verify successful execution for at least five
    different valid locations.
    """

    locations = [
        {
            "latitude": 17.3850,
            "longitude": 78.4867,
        },
        {
            "latitude": 13.0827,
            "longitude": 80.2707,
        },
        {
            "latitude": 19.0760,
            "longitude": 72.8777,
        },
        {
            "latitude": 12.9716,
            "longitude": 77.5946,
        },
        {
            "latitude": 28.6139,
            "longitude": 77.2090,
        },
    ]

    for location in locations:

        response = client.post(
            "/analysis",
            json=location
        )

        # API must succeed
        assert response.status_code == 200

        data = response.json()

        # Complete standardized response
        validate_standard_response(
            data,
            location
        )


# ============================================================
# TEST 2 — INVALID LATITUDE
# ============================================================


def test_invalid_latitude():
    """
    Verify that latitude outside [-90, 90]
    is rejected.
    """

    response = client.post(
        "/analysis",
        json={
            "latitude": 120,
            "longitude": 78,
        }
    )

    assert response.status_code == 422


# ============================================================
# TEST 3 — INVALID LONGITUDE
# ============================================================


def test_invalid_longitude():
    """
    Verify that longitude outside [-180, 180]
    is rejected.
    """

    response = client.post(
        "/analysis",
        json={
            "latitude": 17,
            "longitude": 200,
        }
    )

    assert response.status_code == 422


# ============================================================
# TEST 4 — MISSING LATITUDE
# ============================================================


def test_missing_latitude():
    """
    Verify that latitude is required.
    """

    response = client.post(
        "/analysis",
        json={
            "longitude": 78,
        }
    )

    assert response.status_code == 422


# ============================================================
# TEST 5 — MISSING LONGITUDE
# ============================================================


def test_missing_longitude():
    """
    Verify that longitude is required.
    """

    response = client.post(
        "/analysis",
        json={
            "latitude": 17,
        }
    )

    assert response.status_code == 422


# ============================================================
# TEST 6 — CONSISTENT RESPONSE STRUCTURE
# ============================================================


def test_response_structure_is_consistent():
    """
    Verify that different valid locations return
    exactly the same top-level response structure.
    """

    locations = [
        {
            "latitude": 17.3850,
            "longitude": 78.4867,
        },
        {
            "latitude": 13.0827,
            "longitude": 80.2707,
        },
        {
            "latitude": 19.0760,
            "longitude": 72.8777,
        },
        {
            "latitude": 12.9716,
            "longitude": 77.5946,
        },
        {
            "latitude": 28.6139,
            "longitude": 77.2090,
        },
    ]

    response_keys = []

    for location in locations:

        response = client.post(
            "/analysis",
            json=location
        )

        assert response.status_code == 200

        data = response.json()

        response_keys.append(
            set(data.keys())
        )

    # Every valid location must return
    # the same top-level response structure.
    first_structure = response_keys[0]

    for structure in response_keys[1:]:
        assert structure == first_structure


# ============================================================
# TEST 7 — NO MODULE FAILURE
# ============================================================


def test_complete_pipeline_execution():
    """
    Verify that the complete analysis pipeline executes
    successfully without module/service failures.
    """

    location = {
        "latitude": 17.3850,
        "longitude": 78.4867,
    }

    response = client.post(
        "/analysis",
        json=location
    )

    # Any server-side/module failure should not occur.
    assert response.status_code == 200

    data = response.json()

    # Verify all major modules contributed
    # to the final standardized response.
    assert "site_suitability" in data
    assert "recommended_deployment" in data
    assert "technical_feasibility" in data
    assert "energy_yield" in data
    assert "financial_metrics" in data
    assert "recommendation_reason" in data

    # Response should not contain an error payload.
    assert "error" not in data
