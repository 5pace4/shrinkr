from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from shrinkr.models.url import URLResponse, URLCreate
from shrinkr.repository.create_url import create_short_url
from shrinkr.repository.get_original_url import get_original_url
from shrinkr.repository.get_urls_by_user import get_urls_by_user



router = APIRouter(tags=["urls"], prefix="/urls")

@router.post("/", response_model=URLResponse)
def create_shortend_url(url: URLCreate):
    """Create a shortened URL for the given original URL."""
    try:
        return create_short_url(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}", response_model=list[URLResponse])
def get_urls_for_user(user_id: UUID):
    """Retrieve all shortened URLs created by the given user."""
    rows = get_urls_by_user(user_id)
    return [
        URLResponse(
            user_id=row.user_id,
            original_url=row.long_url,
            shortened_url=row.short_url,
            created_at=row.creation_date.isoformat(),
            expiration_date=row.expiration_date.isoformat(),
            click_count=row.click_count,
        )
        for row in rows
    ]


@router.get("/{short_url}")
def redirect_to_original(short_url: str):
    """Redirect to the original URL for the given short code."""
    row = get_original_url(short_url)
    if row is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    if row.expiration_date < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Short URL has expired")
    # 302, not 301: keeps every click hitting this endpoint so click_count stays accurate.
    return RedirectResponse(url=row.long_url, status_code=302)
