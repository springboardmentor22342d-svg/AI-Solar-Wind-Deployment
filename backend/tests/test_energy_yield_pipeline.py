

import pytest
from backend.app.services.analysis_pipeline import AnalysisPipeline


def test_pipeline_includes_energy_yield():
   

    pipeline = AnalysisPipeline()

    result = pipeline.analyze(
        17.3850,
        78.4867
    )

    # --------------------------------------------------
    # Energy yield must be present
    # --------------------------------------------------

    assert "energy_yield" in result

    energy_yield = result["energy_yield"]

    assert isinstance(energy_yield, dict)

    # --------------------------------------------------
    # Required energy-yield fields
    # --------------------------------------------------

    assert "technology" in energy_yield
    assert "total_annual_energy_mwh" in energy_yield
    assert "total_annual_energy_gwh" in energy_yield

    # --------------------------------------------------
    # Validate data types
    # --------------------------------------------------

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

    # --------------------------------------------------
    # Validate values
    # --------------------------------------------------

    assert len(energy_yield["technology"]) > 0

    assert energy_yield["total_annual_energy_mwh"] > 0

    assert energy_yield["total_annual_energy_gwh"] > 0

    # --------------------------------------------------
    # Verify MWh -> GWh conversion
    # --------------------------------------------------

    expected_gwh = (
    energy_yield["total_annual_energy_mwh"] / 1000
    )

    assert energy_yield["total_annual_energy_gwh"] == pytest.approx(
    expected_gwh,
    abs=0.01
    )