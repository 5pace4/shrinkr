from uuid import UUID

from shrinkr.db.database import session


def increment_click_count(user_id: UUID, short_url: str, current_count: int) -> None:
    """Increment the click counter for the given short code."""
    session.execute(
        """
        UPDATE urls_by_user
        SET click_count = %s
        WHERE user_id = %s AND short_url = %s
        """,
        (current_count + 1, user_id, short_url),
    )
