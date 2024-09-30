from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


def generate_default_username() -> str:
    return f"user_{datetime.now().strftime('%Y%m%d%H%M%S')}"


class UserBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., default_factory=generate_default_username)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    # override
    name: Optional[str]


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: Optional[int] = Field(
        None,
        description="Auto-incremented ID, set by the database",
    )
    couple_id: Optional[int] = Field(
        None,
        description="couple_id is applied by couple_schema",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
    )
