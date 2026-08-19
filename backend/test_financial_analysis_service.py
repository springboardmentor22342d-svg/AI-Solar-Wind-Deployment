from app.financial.financial_analysis_service import FinancialAnalysisService

service = FinancialAnalysisService()

result = service.analyze(

    annual_energy_yield=69921.7,

    electricity_tariff=8,

    installed_capacity=100,

    cost_per_kw=50000,

    installation_percentage=10

)

print(result)