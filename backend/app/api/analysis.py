
from fastapi import APIRouter

from backend.app.schemas.analysis import (
    AnalysisRequest,
    FinalAnalysisResponse
)

from backend.app.services.analysis_pipeline import AnalysisPipeline


router = APIRouter(tags=["Analysis"])

pipeline = AnalysisPipeline()


@router.post(
    "/analysis",
    response_model=FinalAnalysisResponse
)
def analyze(request: AnalysisRequest):

    return pipeline.analyze(
        latitude=request.latitude,
        longitude=request.longitude
    )