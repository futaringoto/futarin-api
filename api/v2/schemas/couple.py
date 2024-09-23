from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


def generate_default_couplename() -> str:
    return f"couple_{datetime.now().strftime('%Y%m%d%H%M%S')}"


class CoupleBase(BaseModel):
    couple_name: str = Field(
        default_factory=generate_default_couplename
    )


class CoupleCreate(CoupleBase):
    pass


class CoupleUpdate(CoupleBase):
    pass


class CoupleResponse(CoupleBase):
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
