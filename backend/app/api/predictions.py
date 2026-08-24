from fastapi import APIRouter
router = APIRouter(prefix="/predictions")
@router.get("/")
def prediction():
    return {
        "message":"Prediction API"
    }