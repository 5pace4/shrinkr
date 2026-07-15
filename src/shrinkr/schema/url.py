from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class URLSchema(BaseModel):
    user_id: UUID
    original_url: str
    shortened_url: str
    created_at: datetime
    expiration_date: datetime
    click_count: int