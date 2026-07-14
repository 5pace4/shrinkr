from uuid import uuid4
from datetime import datetime

from shrinkr.db.database import session
from shrinkr.schema.user import UserSchema
from shrinkr.models.user import UserCreate, UserResponse


def create_user(user: UserCreate) -> UserResponse:
    """Create a new user in the database."""
    new_user = UserSchema(
        id=uuid4(),
        username=user.username,
        email=user.email,
        created_at=datetime.utcnow()
    )

    session.execute(
        """
        INSERT INTO users (id, username, email, created_at)
        VALUES (%s, %s, %s, %s)
        """,
        (new_user.id, new_user.username, new_user.email, new_user.created_at),
    )
    
    return UserResponse(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        created_at=new_user.created_at
    )