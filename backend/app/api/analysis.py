from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.schemas.analysis import AnalysisRequest, AnalysisResponse
from app.services.analysis_service import AnalysisService
from app.services.feature_store_service import FeatureStoreService
from app.auth.security import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/analysis", response_model=AnalysisResponse)
def run_full_analysis(payload: AnalysisRequest, request: Request,
                       current_user: User = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    try:
        builder = request.app.state.feature_builder
        solar_prediction_service = request.app.state.solar_prediction_service
        wind_prediction_service = request.app.state.wind_prediction_service
        land_mask_client = request.app.state.land_mask_client
        feature_store_service = FeatureStoreService(db)

        service = AnalysisService(builder, solar_prediction_service, wind_prediction_service,
                                   land_mask_client, feature_store_service)
        result = service.run_analysis(
            payload.latitude, payload.longitude, payload.project_name,
            payload.installed_capacity_kw, payload.tariff_per_kwh
        )
        return result
    except Exception:
        raise HTTPException(status_code=500, detail="Analysis pipeline failed. Please try again or contact support if the issue persists.")