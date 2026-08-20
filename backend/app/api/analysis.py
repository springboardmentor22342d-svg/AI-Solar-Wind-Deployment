from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.schemas.site import SiteAnalysisResponse
from app.services.analysis_pipeline import AnalysisPipeline
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.models.site_analysis import SiteAnalysis
from typing import List

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=AnalysisResponse)
def analyze_site_workflow(
    request: AnalysisRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Executes the complete site suitability analysis pipeline.
    This unified endpoint accepts coordinates, retrieves all relevant features (solar, wind, terrain),
    evaluates the site against deployment constraints, calculates scores, and returns
    a final deployment recommendation.
    """
    try:
        pipeline = AnalysisPipeline()
        result = pipeline.execute_pipeline(
            latitude=request.latitude,
            longitude=request.longitude,
            site_name=request.site_name
        )

        # Save to Database
        db_analysis = SiteAnalysis(
            user_id=current_user.id,
            site_name=request.site_name or f"Site at {request.latitude}, {request.longitude}",
            latitude=request.latitude,
            longitude=request.longitude,
            solar_irradiance_kwh=result["features"].get("solar_irradiance_kwh"),
            wind_speed_ms=result["features"].get("wind_speed_ms"),
            elevation_m=result["features"].get("elevation_m"),
            slope_deg=result["features"].get("slope_deg"),
            ndvi=result["geospatial"]["ndvi"],
            land_cover_class=result["geospatial"]["land_cover"],
            dist_grid_km=result["features"].get("dist_grid_km"),
            dist_road_km=result["features"].get("dist_road_km"),
            suitability_score=result["evaluation"]["overall_score"],
            recommendation=result["deployment"]["recommended_technology"]
        )
        db.add(db_analysis)
        db.commit()
        db.refresh(db_analysis)

        # Provide the DB ID as the site_id
        result["site_id"] = str(db_analysis.id)

        return result
    except ValueError as e:
        logger.error(f"Validation error in analysis pipeline: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in analysis pipeline: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing the analysis.")


@router.get("/history", response_model=List[SiteAnalysisResponse])
def get_analysis_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get the history of site analyses run by the authenticated user.
    """
    analyses = db.query(SiteAnalysis).filter(SiteAnalysis.user_id == current_user.id).order_by(SiteAnalysis.created_at.desc()).all()
    return analyses

@router.delete("/history/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific site analysis run by the authenticated user.
    """
    analysis = db.query(SiteAnalysis).filter(
        SiteAnalysis.id == analysis_id,
        SiteAnalysis.user_id == current_user.id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found or you do not have permission to delete it.")
        
    db.delete(analysis)
    db.commit()
    return {"message": "Analysis deleted successfully."}
