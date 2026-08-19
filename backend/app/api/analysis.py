from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel, Field

from app.services.analysis_pipeline_service import AnalysisPipelineService

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)

pipeline = AnalysisPipelineService()


class AnalysisRequest(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate between -90 and 90")
    longitude: float = Field(..., description="Longitude coordinate between -180 and 180")


@router.post("/")
def analyze_site(
    request: Optional[AnalysisRequest] = Body(None),
    latitude: Optional[float] = Query(None),
    longitude: Optional[float] = Query(None),
):
    lat = request.latitude if request else latitude
    lon = request.longitude if request else longitude

    if lat is None or lon is None:
        raise HTTPException(
            status_code=400,
            detail="Latitude and Longitude are required."
        )

    if lat < -90 or lat > 90:
        raise HTTPException(
            status_code=400,
            detail="Latitude must be between -90 and 90."
        )

    if lon < -180 or lon > 180:
        raise HTTPException(
            status_code=400,
            detail="Longitude must be between -180 and 180."
        )

    try:
        return pipeline.analyze_site(lat, lon)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )