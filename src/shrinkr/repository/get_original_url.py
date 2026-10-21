from shrinkr.db.database import session


def get_original_url(short_url: str):
    """Retrieve the URL record for the given short code, via the short_url secondary index."""
    result = session.execute(
        """
        SELECT user_id, long_url, expiration_date, click_count
        FROM urls_by_user
        WHERE short_url = %s
        """,
        (short_url,)
    )
    return result.one()
