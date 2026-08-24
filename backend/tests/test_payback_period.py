

import pytest

from backend.app.financial.financial_analysis import (
    FinancialAnalysisService
)


def test_payback_period_calculation():

    service = FinancialAnalysisService()

    result = service.calculate_payback_period(
        total_project_cost_inr=550_000_000,
        annual_revenue_inr=195_660_600
    )

    print("\nPayback Period:")
    print(result)

    expected = (
        550_000_000
        / 195_660_600
    )

    assert result["total_project_cost_inr"] == 550_000_000

    assert result["annual_revenue_inr"] == 195_660_600

    assert result["payback_period_years"] == pytest.approx(
        expected,
        abs=0.01
    )

    assert result["payback_status"] == "Recoverable"


def test_zero_revenue_is_not_recoverable():

    service = FinancialAnalysisService()

    result = service.calculate_payback_period(
        total_project_cost_inr=550_000_000,
        annual_revenue_inr=0
    )

    assert result["payback_period_years"] is None

    assert result["payback_status"] == "Not Recoverable"


def test_negative_revenue_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):

        service.calculate_payback_period(
            total_project_cost_inr=550_000_000,
            annual_revenue_inr=-100_000
        )


def test_negative_project_cost_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):

        service.calculate_payback_period(
            total_project_cost_inr=-550_000_000,
            annual_revenue_inr=195_660_600
        )


def test_zero_project_cost_has_zero_payback():

    service = FinancialAnalysisService()

    result = service.calculate_payback_period(
        total_project_cost_inr=0,
        annual_revenue_inr=195_660_600
    )

    assert result["payback_period_years"] == 0

    assert result["payback_status"] == "Recoverable"
