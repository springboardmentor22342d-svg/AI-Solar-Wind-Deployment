"""
Annual revenue estimation. Deliberately takes only plain numeric
inputs — no dependency on ML/feature modules — so financial models
can be extended or replaced without touching the prediction pipeline.
"""

def estimate_annual_revenue(annual_energy_yield_kwh: float, tariff_per_kwh: float) -> float:
    if annual_energy_yield_kwh is None or tariff_per_kwh is None:
        return 0.0
    return round(annual_energy_yield_kwh * tariff_per_kwh, 2)