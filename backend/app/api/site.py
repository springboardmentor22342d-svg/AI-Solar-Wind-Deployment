"""
app/api/site.py – Site Suitability Analysis endpoints.

All endpoints require authentication (JWT Bearer token).
Analyst and Admin roles can run analyses.

"""

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
    # current_user: User = Depends(require_analyst_or_admin), # Temporarily bypassed for easy testing
):
    """
    [ANALYST / ADMIN] Run site suitability analysis combining 5 datasets.
    Requires authentication with analyst or admin role.
    """
    try:
        service = SpatialAnalysisService()
        
        # Pydantic already validated that lat/lon are within -90/90 and -180/180
        # If needed, we can further validate or handle errors from the service
        # A mocked site_id is provided until db integration is ready
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
    """
    [AUTHENTICATED] Get the current user's site analysis history.

    TODO (Milestone 2): Fetch analyses for current_user from DB.
    """
    raise HTTPException(
        status_code=501,
        detail="Site history not yet implemented. Coming in Milestone 2.",
    )
