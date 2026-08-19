from app.services.analysis_pipeline_service import AnalysisPipelineService

pipeline = AnalysisPipelineService()

result = pipeline.analyze_site(
    latitude=17.3850,
    longitude=78.4867
)

print(result)