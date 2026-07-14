from fastapi import APIRouter, HTTPException

from shrinkr.models.user import UserResponse, UserCreate
from shrinkr.repository.create_user import create_user as create_user_service

router = APIRouter(tags=["users"], prefix="/users")

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    """Create a new user."""
    try:
        return create_user_service(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))