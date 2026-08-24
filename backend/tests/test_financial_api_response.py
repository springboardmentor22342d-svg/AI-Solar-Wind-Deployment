

from backend.app.services.analysis_pipeline import AnalysisPipeline


def test_final_response_contains_financial_information():
    """
    Verify that the standardized final response
    contains financial information.
    """

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        latitude=17.3850,
        longitude=78.4867
    )

    # --------------------------------------------------
    # Financial metrics must be present
    # --------------------------------------------------

    assert "financial_metrics" in result

    financial = result["financial_metrics"]

    assert isinstance(financial, dict)

    # --------------------------------------------------
    # Required financial fields
    # --------------------------------------------------

    assert "annual_revenue" in financial
    assert "estimated_project_cost" in financial
    assert "payback_period" in financial
    assert "roi" in financial

    # --------------------------------------------------
    # Validate data types
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Validate values
    # --------------------------------------------------

    assert financial["annual_revenue"] >= 0

    assert financial["estimated_project_cost"] > 0

    assert financial["payback_period"] >= 0
