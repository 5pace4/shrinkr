from pydantic import BaseModel, Field, HttpUrl
from uuid import UUID

class URLCreate(BaseModel):
    original_url: HttpUrl
    custom_alias: str | None = Field(
        default=None, pattern=r"^[A-Za-z0-9_-]{3,32}$"
    )


class URLResponse(BaseModel):
    user_id: UUID
    original_url: str
    shortened_url: str
    created_at: str
    expiration_date: str
    click_count: int