from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Welcome to the Solar & Wind Deployment Intelligence Platform API"}