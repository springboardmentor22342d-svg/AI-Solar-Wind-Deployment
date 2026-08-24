


from backend.app.services.analysis_pipeline import AnalysisPipeline


def test_complete_analysis_pipeline():

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        latitude=17.3850,
        longitude=78.4867
    )

    # --------------------------------------------------
    # 1. Location
    # --------------------------------------------------

    assert "location" in result

    assert result["location"]["latitude"] == 17.3850
    assert result["location"]["longitude"] == 78.4867

    # --------------------------------------------------
    # 2. Standardized final response
    # --------------------------------------------------

    assert "site_suitability" in result
    assert "recommended_deployment" in result
    assert "technical_feasibility" in result
    assert "energy_yield" in result
    assert "financial_metrics" in result
    assert "recommendation_reason" in result

    # --------------------------------------------------
    # 3. Site Suitability
    # --------------------------------------------------

    site_suitability = result["site_suitability"]

    assert isinstance(site_suitability, dict)

    assert "constraints_satisfied" in site_suitability
    assert "overall_score" in site_suitability
    assert "recommendation" in site_suitability
    assert "failed_constraints" in site_suitability

    # --------------------------------------------------
    # 4. Recommended Deployment
    # --------------------------------------------------

    deployment = result["recommended_deployment"]

    assert isinstance(deployment, str)
    assert len(deployment) > 0

    # --------------------------------------------------
    # 5. Technical Feasibility
    # --------------------------------------------------

    technical = result["technical_feasibility"]

    assert isinstance(technical, dict)

    assert "technically_feasible" in technical
    assert "hard_constraints" in technical
    assert "soft_score" in technical
    assert "decision" in technical

    # --------------------------------------------------
    # 6. Energy Yield
    # --------------------------------------------------

    energy = result["energy_yield"]

    assert isinstance(energy, dict)

    assert "technology" in energy
    assert "total_annual_energy_mwh" in energy
    assert "total_annual_energy_gwh" in energy

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

    # --------------------------------------------------
    # 7. Financial Metrics
    # --------------------------------------------------

    financial = result["financial_metrics"]

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
    assert financial["estimated_project_cost"] > 0
    assert financial["payback_period"] >= 0

    # --------------------------------------------------
    # 8. Recommendation Reason
    # --------------------------------------------------

    reason = result["recommendation_reason"]

    assert isinstance(reason, str)
    assert len(reason) > 0
