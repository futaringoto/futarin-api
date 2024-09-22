from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


def generate_default_username() -> str:
    return f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"


class UserBase(BaseModel):
    couple_id: Optional[int] = Field(
        None,
        description="couple_id is optional",
    )
    username: str = Field(..., default_factory=generate_default_username)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: Optional[int] = Field(
        None,
        description="Auto-incremented ID, set by the database",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
    )
