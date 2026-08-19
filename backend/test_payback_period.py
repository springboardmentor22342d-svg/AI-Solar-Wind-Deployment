from app.financial.payback_period import PaybackPeriodCalculator

calculator = PaybackPeriodCalculator()

years = calculator.calculate(

    total_project_cost=5500000,

    annual_revenue=559373.6

)

print(years)