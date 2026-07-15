from shrinkr.db.database import session

def get_short_url(url: str):
    """Retrieve the short URL for the given original URL."""
    result = session.execute(
        """
        SELECT short_url
        FROM urls_by_user
        WHERE long_url = %s ALLOW FILTERING
        """,
        (url,)
    )
    row = result.one()
    if row:
        return row.short_url
    return None