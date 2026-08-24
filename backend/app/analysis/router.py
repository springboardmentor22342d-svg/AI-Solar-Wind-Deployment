from fastapi import APIRouter
from app.analysis.pipeline import AnalysisPipeline
from app.analysis.schemas import SiteRequest
router = APIRouter()

pipeline = AnalysisPipeline()
@router.post("/analysis")
def analyze(site: SiteRequest):
    return pipeline.analyze(site.dict())