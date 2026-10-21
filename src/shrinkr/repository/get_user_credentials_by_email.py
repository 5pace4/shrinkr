from pydantic import EmailStr

from shrinkr.db.database import session


def get_user_credentials_by_email(email: EmailStr):
    """Retrieve id and hashed password for login verification."""
    result = session.execute(
        """
        SELECT id, password
        FROM users
        WHERE email = %s
        """,
        (email,),
    )
    return result.one()
