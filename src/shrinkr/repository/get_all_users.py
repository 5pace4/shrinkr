from shrinkr.db.database import session

def get_all_users():
    """Retrieve all users from the database."""
    result = session.execute(
        """
        SELECT id, username, email, created_at
        FROM users
        """
    )
    return result.all()