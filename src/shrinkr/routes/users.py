from fastapi import APIRouter, HTTPException

from shrinkr.models.user import UserResponse, UserCreate
from shrinkr.repository.create_user import create_user as create_user_service

router = APIRouter(tags=["users"], prefix="/users")

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    """Create a new user."""
    try:
        return create_user_service(user)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{email}", response_model=UserResponse)
def get_user_by_email(email: str):
    """Retrieve a user by email."""
    from shrinkr.repository.get_user_by_email import get_user_by_email as get_user_by_email_service

    user = get_user_by_email_service(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user