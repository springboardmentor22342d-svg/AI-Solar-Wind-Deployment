from fastapi import APIRouter
router = APIRouter(
    prefix="/features",
    tags=["features"]
)
@router.get("/")
def get_all_features():
    return {
        "message":"This will return all feature records"
        }