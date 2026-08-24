


from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_end_to_end_multiple_sites():
    """
    Verify that the /analysis endpoint works for
    multiple valid locations and returns the
    standardized final response.
    """

    locations = [
        {
            "latitude": 17.3850,
            "longitude": 78.4867
        },
        {
            "latitude": 13.0827,
            "longitude": 80.2707
        },
        {
            "latitude": 19.0760,
            "longitude": 72.8777
        }
    ]

    for location in locations:

        response = client.post(
            "/analysis",
            json=location
        )

        # API request should succeed
        assert response.status_code == 200

        data = response.json()

        # --------------------------------------------------
        # 1. Verify location
        # --------------------------------------------------

        assert "location" in data

        assert data["location"]["latitude"] == location["latitude"]
        assert data["location"]["longitude"] == location["longitude"]

        # -------------------------------------------------- # 
        #  Verify Solar # 
        # --------------------------------------------------

        assert "solar" in data 
        solar = data["solar"] 
        assert "class" in solar 
        assert isinstance( solar["class"], str )
        assert len( solar["class"] ) > 0

        # -------------------------------------------------- 
        # 3. Verify Wind 
        # --------------------------------------------------
       
        assert "wind" in data 
        wind = data["wind"] 
        assert "wind_class" in wind 
        assert isinstance( wind["wind_class"], str ) 
        assert len( wind["wind_class"] ) > 0

        # --------------------------------------------------
        # 2. Verify standardized final response
        # --------------------------------------------------

        assert "site_suitability" in data
        assert "recommended_deployment" in data
        assert "technical_feasibility" in data
        assert "energy_yield" in data
        assert "financial_metrics" in data
        assert "recommendation_reason" in data

        # --------------------------------------------------
        # 3. Verify Site Suitability
        # --------------------------------------------------

        site_suitability = data["site_suitability"]

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

        # --------------------------------------------------
        # 4. Verify Recommended Deployment
        # --------------------------------------------------

        assert isinstance(
            data["recommended_deployment"],
            str
        )

        assert len(data["recommended_deployment"]) > 0

        # --------------------------------------------------
        # 5. Verify Technical Feasibility
        # --------------------------------------------------

        technical_feasibility = data["technical_feasibility"]

        assert "technically_feasible" in technical_feasibility
        assert "hard_constraints" in technical_feasibility
        assert "soft_score" in technical_feasibility
        assert "decision" in technical_feasibility

        assert isinstance(
            technical_feasibility["technically_feasible"],
            bool
        )

        assert isinstance(
            technical_feasibility["hard_constraints"],
            dict
        )

        assert isinstance(
            technical_feasibility["soft_score"],
            (int, float)
        )

        assert isinstance(
            technical_feasibility["decision"],
            str
        )

        # --------------------------------------------------
        # 6. Verify Energy Yield
        # --------------------------------------------------

        energy_yield = data["energy_yield"]

        assert "technology" in energy_yield
        assert "total_annual_energy_mwh" in energy_yield
        assert "total_annual_energy_gwh" in energy_yield

        assert isinstance(
            energy_yield["technology"],
            str
        )

        assert isinstance(
            energy_yield["total_annual_energy_mwh"],
            (int, float)
        )

        assert isinstance(
            energy_yield["total_annual_energy_gwh"],
            (int, float)
        )

        assert energy_yield["total_annual_energy_mwh"] > 0
        assert energy_yield["total_annual_energy_gwh"] > 0

        # --------------------------------------------------
# 7. Verify Financial Metrics
# --------------------------------------------------

        financial_metrics = data["financial_metrics"]

        assert "annual_revenue" in financial_metrics
        assert "estimated_project_cost" in financial_metrics
        assert "payback_period" in financial_metrics
        assert "roi" in financial_metrics

        assert isinstance(
        financial_metrics["annual_revenue"],
            (int, float)
        )

        assert isinstance(
            financial_metrics["estimated_project_cost"],
            (int, float)
        )

        assert isinstance(
            financial_metrics["payback_period"],
            (int, float)
        )

        assert isinstance(
            financial_metrics["roi"],
            (int, float)
        )

        assert financial_metrics["annual_revenue"] >= 0
        assert financial_metrics["estimated_project_cost"] >= 0
        assert financial_metrics["payback_period"] >= 0
        assert financial_metrics["roi"] >= 0

        # --------------------------------------------------
        # 8. Verify Recommendation Reason
        # --------------------------------------------------

        assert isinstance(
            data["recommendation_reason"],
            str
        )

        assert len(data["recommendation_reason"]) > 0


def test_end_to_end_invalid_latitude():
    """
    Latitude must be between -90 and 90.
    """

    response = client.post(
        "/analysis",
        json={
            "latitude": 120,
            "longitude": 78
        }
    )

    assert response.status_code == 422


def test_end_to_end_invalid_longitude():
    """
    Longitude must be between -180 and 180.
    """

    response = client.post(
        "/analysis",
        json={
            "latitude": 17,
            "longitude": 200
        }
    )

    assert response.status_code == 422


def test_end_to_end_missing_latitude():
    """
    Latitude is a required request field.
    """

    response = client.post(
        "/analysis",
        json={
            "longitude": 78
        }
    )

    assert response.status_code == 422


def test_end_to_end_missing_longitude():
    """
    Longitude is a required request field.
    """

    response = client.post(
        "/analysis",
        json={
            "latitude": 17
        }
    )

    assert response.status_code == 422


def test_end_to_end_response_structure():
    """
    Verify that the final API response contains
    exactly the standardized top-level sections.
    """

    response = client.post(
        "/analysis",
        json={
            "latitude": 17.3850,
            "longitude": 78.4867
        }
    )

    assert response.status_code == 200

    data = response.json()

    expected_fields = {
        "location",
        "solar", "wind",
        "site_suitability",
        "recommended_deployment",
        "technical_feasibility",
        "energy_yield",
        "financial_metrics",
        "recommendation_reason"
    }

    assert set(data.keys()) == expected_fields


def test_end_to_end_site_suitability_structure():
    """
    Verify the Site Suitability response structure.
    """

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

    expected_fields = {
        "constraints_satisfied",
        "overall_score",
        "recommendation",
        "failed_constraints"
    }

    assert set(site_suitability.keys()) == expected_fields


def test_end_to_end_technical_feasibility_structure():
    """
    Verify the Technical Feasibility response structure.
    """

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

    expected_fields = {
        "technically_feasible",
        "hard_constraints",
        "soft_score",
        "decision"
    }

    assert set(feasibility.keys()) == expected_fields


def test_end_to_end_energy_yield_structure():
    """
    Verify the Energy Yield response structure.
    """

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

    expected_fields = {
        "technology",
        "total_annual_energy_mwh",
        "total_annual_energy_gwh"
    }

    assert set(energy.keys()) == expected_fields


def test_end_to_end_financial_metrics_structure():
    """
    Verify the Financial Metrics response structure.
    """

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

    expected_fields = {
        "annual_revenue",
        "estimated_project_cost",
        "payback_period",
        "roi"
    }

    assert set(financial.keys()) == expected_fields


def test_end_to_end_recommendation():
    """
    Verify the deployment recommendation and
    recommendation reason.
    """

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

    assert len(
        data["recommended_deployment"]
    ) > 0

    assert isinstance(
        data["recommendation_reason"],
        str
    )

    assert len(
        data["recommendation_reason"]
    ) > 0
