from fastapi import APIRouter

router = APIRouter()



#Home endpoint
@router.get("/")
def home():
    return {
        "message": "Solar & Wind Deployment Intelligence Platform"
    }

 