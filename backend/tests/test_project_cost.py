
import pytest

from backend.app.financial.financial_analysis import (
    FinancialAnalysisService
)


def test_project_cost_estimation():

    service = FinancialAnalysisService()

    result = service.estimate_project_cost(
        installed_capacity_mw=10,
        cost_per_mw_inr=50_000_000,
        additional_installation_percentage=10
    )

    print("\nProject Cost:")
    print(result)

    # Base cost:
    # 10 MW × ₹50,000,000
    # = ₹500,000,000

    # Additional cost:
    # ₹500,000,000 × 10%
    # = ₹50,000,000

    # Total:
    # ₹550,000,000

    assert result["installed_capacity_mw"] == 10

    assert result["cost_per_mw_inr"] == 50_000_000

    assert result["base_project_cost_inr"] == 500_000_000

    assert result["additional_cost_inr"] == 50_000_000

    assert result["estimated_total_project_cost_inr"] == 550_000_000


def test_project_cost_without_additional_installation():

    service = FinancialAnalysisService()

    result = service.estimate_project_cost(
        installed_capacity_mw=10,
        cost_per_mw_inr=50_000_000
    )

    assert result["base_project_cost_inr"] == 500_000_000

    assert result["additional_cost_inr"] == 0

    assert result["estimated_total_project_cost_inr"] == 500_000_000


def test_negative_capacity_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):

        service.estimate_project_cost(
            installed_capacity_mw=-10,
            cost_per_mw_inr=50_000_000
        )


def test_negative_cost_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):

        service.estimate_project_cost(
            installed_capacity_mw=10,
            cost_per_mw_inr=-50_000_000
        )


def test_negative_additional_percentage_is_rejected():

    service = FinancialAnalysisService()

    with pytest.raises(ValueError):

        service.estimate_project_cost(
            installed_capacity_mw=10,
            cost_per_mw_inr=50_000_000,
            additional_installation_percentage=-10
        )
