from fastapi import APIRouter 
router = APIRouter(prefix="/projects")
@router.get("/")
def projects():
    return {
        "message":"Projects API"
    }