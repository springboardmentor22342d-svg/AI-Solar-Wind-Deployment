from app.financial.roi import ROICalculator

calculator = ROICalculator()

roi = calculator.calculate(

    annual_revenue=559373.6,

    total_project_cost=5500000

)

print(roi)