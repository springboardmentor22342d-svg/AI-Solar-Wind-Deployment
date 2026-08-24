from app.services.wind_assessment import classify_wind_site
from app.services.deployment_strategy import deployment_result
print(classify_wind_site(6.5))
print(deployment_result("Excellent","Excellent"))
print(deployment_result("Excellent","Poor"))
print(deployment_result("Poor","Excellent"))