from uuid import UUID

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


def _resolve_custom_alias(alias: str, original_url: str) -> str:
    """Validate that a custom alias is free, or already points at this same URL."""
    existing = get_original_url(alias)
    if existing is not None and existing.long_url != original_url:
        raise ValueError(f"Alias '{alias}' is already taken")
    return alias


def create_short_url(url: URLCreate, user_id: UUID) -> URLResponse:
    original_url = str(url.original_url)
    shortend_url = (
        _resolve_custom_alias(url.custom_alias, original_url)
        if url.custom_alias
        else _resolve_short_code(original_url)
    )
    created_at = datetime.utcnow()
    new_url = URLSchema(
        user_id=user_id,
        original_url=original_url,
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
