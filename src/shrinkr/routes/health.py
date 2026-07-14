from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["health"], prefix="/health")

@router.get("/")
def health_check():
    return {"status": "healthy"}