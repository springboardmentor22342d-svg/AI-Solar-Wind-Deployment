from app.financial.financial_analysis_service import run_financial_analysis

# Baseline
print(run_financial_analysis(7_301_206, 5000, "Solar"))

# Higher tariff -> revenue and ROI should increase, payback should shrink
print(run_financial_analysis(7_301_206, 5000, "Solar", tariff_per_kwh=5.0))

# Larger capacity/cost -> payback should lengthen if revenue doesn't scale proportionally
print(run_financial_analysis(7_301_206, 10000, "Solar"))