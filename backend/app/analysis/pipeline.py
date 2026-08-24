from app.services.solar_services import SolarFeatureService
from app.services.wind_assessment import WindAssessmentService
from app.evaluation.evaluator import SiteEvaluator
from app.evaluation.recommendation import recommend

class AnalysisPipeline:
    def analyze(self,site):
        solar_service = SolarFeatureService()
        wind_service = WindAssessmentService()
        evaluator = SiteEvaluator()
        recommendation = recommend()

        solar_data = solar_service.get_solar_data(site["latitude"],site["longitude"])
        wind_data = wind_service.get_wind_data
        site_score = evaluator.evaluate(solar_data,wind_data)
        deployment = recommendation.generate(site_score)

        return {
            "site": site,
            "solar_features": solar_data,
            "wind_feature": wind_data,
            "site_score": site_score,
            "deployment": deployment
        }