


from backend.app.services.analysis_pipeline import AnalysisPipeline


def test_pipeline_includes_feasibility():
    """
    Verify that the AnalysisPipeline includes
    technical feasibility in the standardized
    final analysis response.
    """

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        17.3850,
        78.4867
    )

    # --------------------------------------------------
    # Standardized response should include
    # technical feasibility
    # --------------------------------------------------

    assert "technical_feasibility" in result

    feasibility = result["technical_feasibility"]

    assert isinstance(feasibility, dict)

    # --------------------------------------------------
    # Required feasibility fields
    # --------------------------------------------------

    assert "technically_feasible" in feasibility
    assert "hard_constraints" in feasibility
    assert "soft_score" in feasibility
    assert "decision" in feasibility

    # --------------------------------------------------
    # Validate field types
    # --------------------------------------------------

    assert isinstance(
        feasibility["technically_feasible"],
        bool
    )

    assert isinstance(
        feasibility["hard_constraints"],
        dict
    )

    assert isinstance(
        feasibility["soft_score"],
        (int, float)
    )

    assert isinstance(
        feasibility["decision"],
        str
    )

    # --------------------------------------------------
    # Validate values
    # --------------------------------------------------

    assert feasibility["soft_score"] >= 0

    assert len(feasibility["decision"]) > 0
