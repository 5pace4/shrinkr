from shrinkr.db.database import session
from shrinkr.repository.get_user_by_email import get_user_by_email

def delete_user_by_email(email: str) -> bool:
    """Delete a user from the database by email."""
    user = get_user_by_email(email)
    if not user:
        return False  # User not found

    session.execute(
        """
        DELETE FROM users
        WHERE id = %s
        """,
        (user.id,),
    )
    return True