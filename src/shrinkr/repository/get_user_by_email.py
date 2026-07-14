from pydantic import EmailStr

from shrinkr.db.database import session
from shrinkr.models.user import UserResponse

def get_user_by_email(email: EmailStr) -> UserResponse:
    """Retrieve a user from the database by email."""
    result = session.execute(
        """
        SELECT id, username, email, password, created_at
        FROM users
        WHERE email = %s
        """,
        (email,),
    )
    row = result.one()
    if row:
        return UserResponse(
            id=row.id,
            username=row.username,
            email=row.email,
            created_at=row.created_at
        )
    return None