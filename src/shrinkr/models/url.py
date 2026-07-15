from pydantic import BaseModel
from uuid import UUID

class URLCreate(BaseModel):
    original_url: str
    user_id: UUID


class URLResponse(BaseModel):
    user_id: UUID
    original_url: str
    shortened_url: str
    created_at: str
    expiration_date: str
    click_count: int