from datetime import datetime
from pydantic import BaseModel, EmailStr
from uuid import UUID


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    

class UserResponse(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    created_at: datetime


