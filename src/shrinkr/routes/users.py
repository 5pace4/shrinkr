from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request

from shrinkr.models.user import LoginRequest, Token, UserResponse, UserCreate
from shrinkr.rate_limit import limiter
from shrinkr.repository.create_user import create_user as create_user_service
from shrinkr.repository.get_user_by_email import get_user_by_email as get_user_by_email_service
from shrinkr.repository.get_user_credentials_by_email import get_user_credentials_by_email
from shrinkr.repository.get_all_users import get_all_users as get_all_users_service
from shrinkr.repository.delete_user import delete_user_by_email
from shrinkr.services.auth_service import create_access_token, get_current_user_id
from shrinkr.services.password_service import verify_password

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


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, credentials: LoginRequest):
    """Authenticate a user and issue a bearer access token."""
    row = get_user_credentials_by_email(credentials.email)
    if row is None or not verify_password(credentials.password, row.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return Token(access_token=create_access_token(row.id))


@router.get("/{email}", response_model=UserResponse)
def get_user_by_email(email: str):
    """Retrieve a user by email."""

    user = get_user_by_email_service(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/", response_model=list[UserResponse])
def get_all_users(current_user_id: UUID = Depends(get_current_user_id)):
    """Retrieve all users."""

    return get_all_users_service()


@router.delete("/{email}")
def delete_user(email: str, current_user_id: UUID = Depends(get_current_user_id)):
    """Delete a user account. A user may only delete their own account."""
    user = get_user_by_email_service(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.id != current_user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own account")
    delete_user_by_email(email)
    return {"message": f"User with email {email} has been deleted."}
