from app.services.deployment_strategy import DeploymentStrategyService

service = DeploymentStrategyService()

result = service.recommend_deployment(
    solar_irradiance=7.5,
    wind_speed=4.5,
)

print(result)