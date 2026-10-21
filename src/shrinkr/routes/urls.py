from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from shrinkr.models.url import URLResponse, URLCreate
from shrinkr.rate_limit import limiter
from shrinkr.repository.create_url import create_short_url
from shrinkr.repository.delete_url import delete_url
from shrinkr.repository.get_original_url import get_original_url
from shrinkr.repository.get_urls_by_user import get_urls_by_user
from shrinkr.repository.increment_click_count import increment_click_count
from shrinkr.services.auth_service import get_current_user_id



router = APIRouter(tags=["urls"], prefix="/urls")

@router.post("/", response_model=URLResponse)
@limiter.limit("20/minute")
def create_shortend_url(request: Request, url: URLCreate, current_user_id: UUID = Depends(get_current_user_id)):
    """Create a shortened URL owned by the authenticated user."""
    try:
        return create_short_url(url, current_user_id)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{user_id}", response_model=list[URLResponse])
def get_urls_for_user(user_id: UUID, current_user_id: UUID = Depends(get_current_user_id)):
    """Retrieve all shortened URLs created by the given user."""
    if user_id != current_user_id:
        raise HTTPException(status_code=403, detail="You can only view your own URLs")
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


@router.delete("/{short_url}")
def delete_shortend_url(short_url: str, current_user_id: UUID = Depends(get_current_user_id)):
    """Delete a shortened URL owned by the authenticated user."""
    row = get_original_url(short_url)
    if row is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    if row.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="You can only delete your own URLs")
    delete_url(current_user_id, short_url)
    return {"message": f"Short URL {short_url} has been deleted."}


@router.get("/{short_url}")
@limiter.limit("60/minute")
def redirect_to_original(request: Request, short_url: str):
    """Redirect to the original URL for the given short code."""
    row = get_original_url(short_url)
    if row is None:
        raise HTTPException(status_code=404, detail="Short URL not found")
    if row.expiration_date < datetime.utcnow():
        raise HTTPException(status_code=410, detail="Short URL has expired")
    increment_click_count(row.user_id, short_url, row.click_count)
    # 302, not 301: keeps every click hitting this endpoint so click_count stays accurate.
    return RedirectResponse(url=row.long_url, status_code=302)
