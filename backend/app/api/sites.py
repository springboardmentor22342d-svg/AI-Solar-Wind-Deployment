from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import SiteAnalysisRequest, SiteAnalysisResponse
from app.auth.dependencies import get_current_user
from app.auth.roles import require_analyst_or_admin
from app.models.user import User

router = APIRouter()

from app.services.spatial.analysis_coordinator import SpatialAnalysisService
from app.schemas.site import DetailedSiteAnalysisResponse

@router.post("/analyze", response_model=DetailedSiteAnalysisResponse)
def analyze_site_suitability(
    request: SiteAnalysisRequest,
    db: Session = Depends(get_db),
):
    try:
        service = SpatialAnalysisService()
        mock_site_id = 1
        report = service.run_suitability_analysis(
            site_id=mock_site_id,
            lat=request.latitude,
            lon=request.longitude
        )
        return report
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history", response_model=List[SiteAnalysisResponse])
def get_site_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    raise HTTPException(
        status_code=501,
        detail="Site history not yet implemented. Coming in Milestone 2.",
    )
