from app.financial.revenue import estimate_annual_revenue
from app.financial.payback import calculate_payback_period
from app.financial.roi import calculate_roi

def test_revenue_calculation():
    assert estimate_annual_revenue(1_000_000, 3.5) == 3_500_000.0

def test_payback_zero_revenue():
    assert calculate_payback_period(1_000_000, 0) is None

def test_payback_negative_revenue():
    assert calculate_payback_period(1_000_000, -500) is None

def test_roi_positive():
    roi = calculate_roi(1_000_000, 200_000)
    assert roi > 0