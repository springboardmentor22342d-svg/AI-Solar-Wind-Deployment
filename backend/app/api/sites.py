from fastapi import APIRouter
router = APIRouter(prefix="/sites")
@router.get("/")
def sites():
    return {
        "message":"Sites API"
    }