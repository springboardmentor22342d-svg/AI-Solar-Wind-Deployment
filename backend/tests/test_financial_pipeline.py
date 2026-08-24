

from backend.app.services.analysis_pipeline import AnalysisPipeline


def test_financial_analysis_is_generated_in_pipeline():
    """
    Verify that the complete analysis pipeline
    generates financial metrics after energy yield.
    """

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        latitude=17.3850,
        longitude=78.4867
    )

    # Financial analysis should exist
    assert "financial_metrics" in result

    # Energy yield should exist before financial metrics
    assert "energy_yield" in result

    financial = result["financial_metrics"]

    assert isinstance(financial, dict)


def test_financial_revenue_uses_energy_yield():
    """
    Verify that annual revenue is generated from
    the energy yield produced by the pipeline.
    """

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        latitude=17.3850,
        longitude=78.4867
    )

    energy_yield = result["energy_yield"]
    financial = result["financial_metrics"]

    # Required energy-yield value
    assert "total_annual_energy_mwh" in energy_yield

    # Required financial value
    assert "annual_revenue" in financial

    energy_mwh = energy_yield["total_annual_energy_mwh"]
    annual_revenue = financial["annual_revenue"]

    assert isinstance(energy_mwh, (int, float))
    assert isinstance(annual_revenue, (int, float))

    assert energy_mwh > 0
    assert annual_revenue >= 0


def test_project_cost_is_generated():
    """
    Verify that project cost is generated
    by the financial analysis.
    """

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        latitude=17.3850,
        longitude=78.4867
    )

    financial = result["financial_metrics"]

    assert "estimated_project_cost" in financial

    project_cost = financial["estimated_project_cost"]

    assert isinstance(project_cost, (int, float))
    assert project_cost > 0


def test_payback_period_is_generated():
    """
    Verify that payback period is calculated.
    """

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        latitude=17.3850,
        longitude=78.4867
    )

    financial = result["financial_metrics"]

    assert "payback_period" in financial

    payback = financial["payback_period"]

    assert isinstance(payback, (int, float))
    assert payback >= 0


def test_roi_is_generated():
    """
    Verify that ROI is calculated.
    """

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        latitude=17.3850,
        longitude=78.4867
    )

    financial = result["financial_metrics"]

    assert "roi" in financial

    roi = financial["roi"]

    assert isinstance(roi, (int, float))
