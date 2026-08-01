from fastapi import APIRouter, Request, HTTPException
from app.schemas.analysis import AnalysisRequest
from app.services.analysis_service import AnalysisService

router = APIRouter()

@router.post("/analysis")
def run_full_analysis(payload: AnalysisRequest, request: Request):
    try:
        builder = request.app.state.feature_builder
        solar_prediction_service = request.app.state.solar_prediction_service
        wind_prediction_service = request.app.state.wind_prediction_service
        service = AnalysisService(builder, solar_prediction_service, wind_prediction_service)
        result = service.run_analysis(payload.latitude, payload.longitude, payload.project_name)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis pipeline failed: {str(e)}")