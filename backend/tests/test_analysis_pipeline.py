


from backend.app.services.analysis_pipeline import AnalysisPipeline


pipeline = AnalysisPipeline()


def test_pipeline():

    result = pipeline.analyze(
        17.3850,
        78.4867
    )

    # Location
    assert "location" in result
    assert result["location"]["latitude"] == 17.3850
    assert result["location"]["longitude"] == 78.4867

    # Site Suitability
    assert "site_suitability" in result
    assert "constraints_satisfied" in result["site_suitability"]
    assert "overall_score" in result["site_suitability"]
    assert "recommendation" in result["site_suitability"]

    # Recommended Deployment
    assert "recommended_deployment" in result
    assert result["recommended_deployment"] in [
        "Solar",
        "Wind",
        "Hybrid",
        "Not Recommended"
    ]

    # Technical Feasibility
    assert "technical_feasibility" in result
    assert "technically_feasible" in result["technical_feasibility"]

    # Energy Yield
    assert "energy_yield" in result
    assert "technology" in result["energy_yield"]
    assert "total_annual_energy_mwh" in result["energy_yield"]
    assert "total_annual_energy_gwh" in result["energy_yield"]

    # Financial Metrics
    assert "financial_metrics" in result

    assert "annual_revenue" in result["financial_metrics"]
    assert "estimated_project_cost" in result["financial_metrics"]
    assert "payback_period" in result["financial_metrics"]
    assert "roi" in result["financial_metrics"]

    # Recommendation Reason
    assert "recommendation_reason" in result
    assert isinstance(
        result["recommendation_reason"],
        str
    )
