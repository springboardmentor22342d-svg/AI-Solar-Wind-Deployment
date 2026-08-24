from fastapi import APIRouter
router = APIRouter()
@router.get("/")
def home():
    return {
        "message":"Solar & wind Deployment Intelligence Platform Backend"
    }