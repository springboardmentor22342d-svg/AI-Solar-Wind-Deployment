from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def home():
    return {
        "message": "Solar & Wind Deployment Intelligence Platform"
    }

@router.get("/health")
def health():
    return {
        "status": "Running"
    }

@router.get("/about")
def about():
    return {
        "project": "Solar & Wind Deployment Intelligence Platform"
    }