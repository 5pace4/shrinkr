from pydantic import EmailStr

from shrinkr.repository.get_user_by_email import get_user_by_email


def is_existing_user(email: EmailStr) -> bool:
    """Return True when a user with this email already exists."""
    return get_user_by_email(email) is not None