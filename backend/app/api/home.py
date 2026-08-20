from fastapi import APIRouter

router = APIRouter()

@router.get(
    "/",
    summary="API Health Check",
    tags=["Home"],
)
def read_home():
    return {"message": "API is running"}
