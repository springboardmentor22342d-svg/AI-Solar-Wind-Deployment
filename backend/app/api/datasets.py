from fastapi import APIRouter
router = APIRouter(prefix="/datasets")
@router.get("/")
def get_datasets():
    return {
        "message":"Dataset API is working"
    }