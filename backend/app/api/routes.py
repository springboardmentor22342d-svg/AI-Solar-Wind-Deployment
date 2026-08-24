from fastapi import APIRouter
router = APIRouter()
@router.get("/health")
def health():
    return {
        "status":"OK","message":"Backend is working successfully"
    }