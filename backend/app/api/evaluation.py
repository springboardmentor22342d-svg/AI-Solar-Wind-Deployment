from fastapi import APIRouter

from app.schemas.evaluation import SiteEvaluationRequest

from app.services.evaluation_service import EvaluationService


router = APIRouter(

    prefix="/evaluation",

    tags=["Evaluation"]

)

service = EvaluationService()


@router.post("/evaluate-site")
def evaluate_site(

    request: SiteEvaluationRequest

):

    return service.evaluate_site(

        request.latitude,

        request.longitude

    )