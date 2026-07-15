from shrinkr.db.database import session
from shrinkr.models.url import URLCreate, URLResponse
from shrinkr.schema.url import URLSchema
from datetime import datetime, timedelta
from shrinkr.repository.get_original_url import get_original_url
from shrinkr.services.url_service import make_shortend_url

MAX_COLLISION_RETRIES = 5


def _resolve_short_code(original_url: str) -> str:
    """Find a short code for original_url, salting the hash on collision with a different URL."""
    for salt in range(MAX_COLLISION_RETRIES + 1):
        candidate = make_shortend_url(original_url, salt)
        existing = get_original_url(candidate)
        if existing is None or existing.long_url == original_url:
            return candidate
    raise RuntimeError(
        f"Could not find a free short code for {original_url!r} after {MAX_COLLISION_RETRIES} retries"
    )


def create_short_url(url: URLCreate) -> URLResponse:
    shortend_url = _resolve_short_code(url.original_url)
    created_at = datetime.utcnow()
    new_url = URLSchema(
        user_id=url.user_id,
        original_url=url.original_url,
        shortened_url=shortend_url,
        created_at= created_at,
        expiration_date=created_at + timedelta(days=30),
        click_count=0
    )


    session.execute(
        """
        INSERT INTO urls_by_user (user_id, long_url, short_url, creation_date, expiration_date, click_count)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (new_url.user_id, new_url.original_url, new_url.shortened_url, new_url.created_at, new_url.expiration_date, new_url.click_count),
    )   

    response_data = URLResponse(
        user_id=new_url.user_id,
        original_url=new_url.original_url,
        shortened_url=new_url.shortened_url,
        created_at=new_url.created_at.isoformat(),
        expiration_date=new_url.expiration_date.isoformat(),
        click_count=new_url.click_count
    )
    return response_data
