from uuid import UUID

from shrinkr.db.database import session


def get_urls_by_user(user_id: UUID):
    """Retrieve all URL records created by the given user."""
    result = session.execute(
        """
        SELECT user_id, long_url, short_url, creation_date, expiration_date, click_count
        FROM urls_by_user
        WHERE user_id = %s
        """,
        (user_id,)
    )
    return list(result)
