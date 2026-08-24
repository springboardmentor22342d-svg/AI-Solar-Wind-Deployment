


import pytest

from backend.app.financial.financial_analysis import (
    FinancialAnalysisService
)


def test_higher_tariff_increases_revenue_and_roi():
    service = FinancialAnalysisService()

    energy_mwh = 39132.12
    project_cost = 1_100_000_000

    # Base tariff
    base_revenue = service.estimate_annual_revenue(
        annual_energy_mwh=energy_mwh,
        electricity_tariff_inr_per_kwh=5
    )

    base_financial = service.calculate_roi(
        total_project_cost_inr=project_cost,
        annual_revenue_inr=(
            base_revenue["estimated_annual_revenue_inr"]
        )
    )

    # Higher tariff
    higher_revenue = service.estimate_annual_revenue(
        annual_energy_mwh=energy_mwh,
        electricity_tariff_inr_per_kwh=7
    )

    higher_financial = service.calculate_roi(
        total_project_cost_inr=project_cost,
        annual_revenue_inr=(
            higher_revenue[
                "estimated_annual_revenue_inr"
            ]
        )
    )

    assert (
        higher_revenue["estimated_annual_revenue_inr"]
        > base_revenue["estimated_annual_revenue_inr"]
    )

    assert (
        higher_financial["roi_percentage"]
        > base_financial["roi_percentage"]
    )


def test_higher_tariff_reduces_payback_period():
    service = FinancialAnalysisService()

    energy_mwh = 39132.12
    project_cost = 1_100_000_000

    base_revenue = service.estimate_annual_revenue(
        annual_energy_mwh=energy_mwh,
        electricity_tariff_inr_per_kwh=5
    )

    higher_revenue = service.estimate_annual_revenue(
        annual_energy_mwh=energy_mwh,
        electricity_tariff_inr_per_kwh=7
    )

    base_payback = service.calculate_payback_period(
        total_project_cost_inr=project_cost,
        annual_revenue_inr=(
            base_revenue["estimated_annual_revenue_inr"]
        )
    )

    higher_payback = service.calculate_payback_period(
        total_project_cost_inr=project_cost,
        annual_revenue_inr=(
            higher_revenue["estimated_annual_revenue_inr"]
        )
    )

    assert (
        higher_payback["payback_period_years"]
        < base_payback["payback_period_years"]
    )


def test_lower_tariff_reduces_revenue_and_roi():
    service = FinancialAnalysisService()

    energy_mwh = 39132.12
    project_cost = 1_100_000_000

    base_revenue = service.estimate_annual_revenue(
        annual_energy_mwh=energy_mwh,
        electricity_tariff_inr_per_kwh=5
    )

    lower_revenue = service.estimate_annual_revenue(
        annual_energy_mwh=energy_mwh,
        electricity_tariff_inr_per_kwh=3
    )

    base_roi = service.calculate_roi(
        total_project_cost_inr=project_cost,
        annual_revenue_inr=(
            base_revenue["estimated_annual_revenue_inr"]
        )
    )

    lower_roi = service.calculate_roi(
        total_project_cost_inr=project_cost,
        annual_revenue_inr=(
            lower_revenue["estimated_annual_revenue_inr"]
        )
    )

    assert (
        lower_revenue["estimated_annual_revenue_inr"]
        < base_revenue["estimated_annual_revenue_inr"]
    )

    assert (
        lower_roi["roi_percentage"]
        < base_roi["roi_percentage"]
    )


def test_higher_capacity_increases_project_cost():
    service = FinancialAnalysisService()

    base = service.estimate_project_cost(
        installed_capacity_mw=20,
        cost_per_mw_inr=50_000_000,
        additional_installation_percentage=10
    )

    higher_capacity = service.estimate_project_cost(
        installed_capacity_mw=30,
        cost_per_mw_inr=50_000_000,
        additional_installation_percentage=10
    )

    assert (
        higher_capacity[
            "estimated_total_project_cost_inr"
        ]
        > base[
            "estimated_total_project_cost_inr"
        ]
    )


def test_project_cost_change_affects_payback_and_roi():
    service = FinancialAnalysisService()

    annual_revenue = 195_660_600

    lower_cost = 800_000_000
    higher_cost = 1_100_000_000

    lower_cost_payback = service.calculate_payback_period(
        total_project_cost_inr=lower_cost,
        annual_revenue_inr=annual_revenue
    )

    higher_cost_payback = service.calculate_payback_period(
        total_project_cost_inr=higher_cost,
        annual_revenue_inr=annual_revenue
    )

    lower_cost_roi = service.calculate_roi(
        total_project_cost_inr=lower_cost,
        annual_revenue_inr=annual_revenue
    )

    higher_cost_roi = service.calculate_roi(
        total_project_cost_inr=higher_cost,
        annual_revenue_inr=annual_revenue
    )

    assert (
        higher_cost_payback["payback_period_years"]
        > lower_cost_payback["payback_period_years"]
    )

    assert (
        higher_cost_roi["roi_percentage"]
        < lower_cost_roi["roi_percentage"]
    )


def test_payback_calculation_is_correct():
    service = FinancialAnalysisService()

    project_cost = 1_100_000_000
    annual_revenue = 195_660_600

    result = service.calculate_payback_period(
        total_project_cost_inr=project_cost,
        annual_revenue_inr=annual_revenue
    )

    expected = project_cost / annual_revenue

    assert result["payback_period_years"] == pytest.approx(
        expected,
        abs=0.01
    )

    assert result["payback_status"] == "Recoverable"
