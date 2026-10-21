from uuid import UUID

from shrinkr.db.database import session


def delete_url(user_id: UUID, short_url: str) -> None:
    """Delete a URL record owned by the given user."""
    session.execute(
        """
        DELETE FROM urls_by_user
        WHERE user_id = %s AND short_url = %s
        """,
        (user_id, short_url),
    )
