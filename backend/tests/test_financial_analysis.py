


import pytest

from backend.app.financial.financial_analysis import (
    FinancialAnalysisService
)


def test_annual_revenue_estimation():

    service = FinancialAnalysisService()

    result = service.estimate_annual_revenue(
        annual_energy_mwh=28382.4,
        electricity_tariff_inr_per_kwh=5.0
    )

    print("\nAnnual Revenue:")
    print(result)

    # 28,382.4 MWh = 28,382,400 kWh
    # Revenue = 28,382,400 × ₹5
    expected_revenue = 28382.4 * 1000 * 5.0

    assert result["annual_energy_mwh"] == 28382.4
    assert result["annual_energy_kwh"] == 28382400
    assert result["electricity_tariff_inr_per_kwh"] == 5.0

    assert result["estimated_annual_revenue_inr"] == pytest.approx(
        expected_revenue,
        rel=1e-6
    )


def test_zero_energy_gives_zero_revenue():

    service = FinancialAnalysisService()

    result = service.estimate_annual_revenue(
        annual_energy_mwh=0,
        electricity_tariff_inr_per_kwh=5.0
    )

    assert result["estimated_annual_revenue_inr"] == 0


def test_negative_energy_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):
        service.estimate_annual_revenue(
            annual_energy_mwh=-100,
            electricity_tariff_inr_per_kwh=5.0
        )


def test_negative_tariff_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):
        service.estimate_annual_revenue(
            annual_energy_mwh=10000,
            electricity_tariff_inr_per_kwh=-5.0
        )



def test_roi_calculation():

    service = FinancialAnalysisService()

    result = service.calculate_roi(
        total_project_cost_inr=100000000,
        annual_revenue_inr=20000000
    )

    print("\nROI:")
    print(result)

    # ROI = (20,000,000 / 100,000,000) × 100
    expected_roi = 20.0

    assert result["total_project_cost_inr"] == 100000000
    assert result["annual_revenue_inr"] == 20000000

    assert result["roi_percentage"] == pytest.approx(
        expected_roi,
        rel=1e-6
    )


def test_zero_annual_revenue_gives_zero_roi():

    service = FinancialAnalysisService()

    result = service.calculate_roi(
        total_project_cost_inr=100000000,
        annual_revenue_inr=0
    )

    assert result["roi_percentage"] == 0


def test_negative_project_cost_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):
        service.calculate_roi(
            total_project_cost_inr=-100000000,
            annual_revenue_inr=20000000
        )


def test_zero_project_cost_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):
        service.calculate_roi(
            total_project_cost_inr=0,
            annual_revenue_inr=20000000
        )


def test_negative_annual_revenue_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):
        service.calculate_roi(
            total_project_cost_inr=100000000,
            annual_revenue_inr=-20000000
        )
