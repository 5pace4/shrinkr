from fastapi import APIRouter, HTTPException
from shrinkr.models.url import URLResponse, URLCreate
from shrinkr.repository.create_url import create_short_url



router = APIRouter(tags=["urls"], prefix="/urls")

@router.post("/", response_model=URLResponse)
def create_shortend_url(url: URLCreate):
    """Create a shortened URL for the given original URL."""
    try:
        return create_short_url(url)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    