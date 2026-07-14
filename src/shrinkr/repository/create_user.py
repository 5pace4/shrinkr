from uuid import uuid4
from datetime import datetime

from shrinkr.db.database import session
from shrinkr.schema.user import UserSchema
from shrinkr.models.user import UserCreate, UserResponse
from shrinkr.services.user_service import is_existing_user

def create_user(user: UserCreate) -> UserResponse:
    """Create a new user in the database."""

    if is_existing_user(user.email):
        raise ValueError("User with this email already exists")

    new_user = UserSchema(
        id=uuid4(),
        username=user.username,
        email=user.email,
        password=user.password,
        created_at=datetime.utcnow()
    )
    
    session.execute(
        """
        INSERT INTO users (id, username, email, password, created_at)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (new_user.id, new_user.username, new_user.email, new_user.password, new_user.created_at),
    )
    
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        created_at=new_user.created_at
    )