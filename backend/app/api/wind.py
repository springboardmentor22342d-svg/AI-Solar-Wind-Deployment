"""
app/api/wind.py – Wind Prediction endpoints.

All endpoints require authentication (JWT Bearer token).
Analyst and Admin roles can run predictions.

"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import WindPredictionRequest, WindPredictionResponse
from app.auth.dependencies import get_current_user
from app.auth.roles import require_analyst_or_admin
from app.models.user import User

router = APIRouter()


@router.post("/predict", response_model=WindPredictionResponse)
def predict_wind_yield(
    request: WindPredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
):
    """
    [ANALYST / ADMIN] Run wind prediction model for a given location.
    Requires authentication with analyst or admin role.

    TODO (Milestone 2): Load ML model, run inference, save to DB, return result.
    """
    raise HTTPException(status_code=501, detail="Wind prediction model not yet implemented. Coming in Milestone 2.")


@router.get("/history", response_model=List[WindPredictionResponse])
def get_wind_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    [AUTHENTICATED] Get the current user's wind prediction history.

    TODO (Milestone 2): Fetch predictions for current_user from DB.
    """
    raise HTTPException(status_code=501, detail="Wind history not yet implemented. Coming in Milestone 2.")
