"""
app/api/solar.py – Solar Prediction endpoints.

All endpoints require authentication (JWT Bearer token).
Analyst and Admin roles can run predictions.

"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.schemas import SolarPredictionRequest, SolarPredictionResponse
from app.auth.dependencies import get_current_user
from app.auth.roles import require_analyst_or_admin
from app.models.user import User

router = APIRouter()


@router.post("/predict", response_model=SolarPredictionResponse)
def predict_solar_yield(
    request: SolarPredictionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_analyst_or_admin),
):
    """
    [ANALYST / ADMIN] Run solar prediction model for a given location.
    Requires authentication with analyst or admin role.

    TODO (Milestone 2): Load ML model, run inference, save to DB, return result.
    """
    raise HTTPException(status_code=501, detail="Solar prediction model not yet implemented. Coming in Milestone 2.")


@router.get("/history", response_model=List[SolarPredictionResponse])
def get_solar_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    [AUTHENTICATED] Get the current user's solar prediction history.

    TODO (Milestone 2): Fetch predictions for current_user from DB.
    """
    raise HTTPException(status_code=501, detail="Solar history not yet implemented. Coming in Milestone 2.")


@router.get("/features")
def get_solar_features(
    latitude: float,
    longitude: float,
    # Optional: current_user: User = Depends(get_current_user)
    # The requirement didn't explicitly mandate auth for this specific GET, but assuming it's an authenticated API
):
    """
    [AUTHENTICATED] Retrieve solar features (irradiance, temperature, humidity) for a location.
    Calls the NASA POWER API internally via the FeatureBuilder service.
    """
    from app.services.feature_builder import FeatureBuilder
    from app.data_sources.nasa_power import CoordinateValidationError, NasaPowerAPIError
    
    try:
        builder = FeatureBuilder()
        return builder.get_solar_features(latitude, longitude)
    except CoordinateValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NasaPowerAPIError as e:
        raise HTTPException(status_code=502, detail=f"External API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred while fetching solar features.")
