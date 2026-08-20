from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import SolarPredictionRequest, SolarPredictionResponse
from app.schemas import SiteAnalysisRequest, SiteAnalysisResponse
from app.auth.dependencies import get_current_user
from app.auth.roles import require_analyst_or_admin
from app.models.user import User

router = APIRouter()


@router.post("/solar", response_model=SolarPredictionResponse)
def predict_solar(
    request: SolarPredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
):
    raise HTTPException(status_code=501, detail="Solar prediction not yet implemented. Coming in Milestone 2.")


@router.get("/solar/history", response_model=List[SolarPredictionResponse])
def solar_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=501, detail="Solar history not yet implemented. Coming in Milestone 2.")


@router.post("/wind")
def predict_wind(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
):
    raise HTTPException(status_code=501, detail="Wind prediction not yet implemented. Coming in Milestone 2.")


@router.get("/wind/history")
def wind_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    raise HTTPException(status_code=501, detail="Wind history not yet implemented. Coming in Milestone 2.")
