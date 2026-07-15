from shrinkr.db.database import session
from shrinkr.models.url import URLCreate, URLResponse
from shrinkr.schema.url import URLSchema
from datetime import datetime, timedelta
from shrinkr.services.url_service import make_shortend_url


def create_short_url(url: URLCreate) -> URLResponse:
    shortend_url = make_shortend_url(url.original_url)
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
