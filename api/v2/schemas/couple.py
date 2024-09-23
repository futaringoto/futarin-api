from typing import Optional
from pydantic import BaseModel, Extra, Field
from datetime import datetime


def generate_default_couplename() -> str:
    return f"couple_{datetime.now().strftime('%Y%m%d%H%M%S')}"


class CoupleBase(BaseModel, extra=Extra.forbid):
    couple_name: str = Field(
        default_factory=generate_default_couplename
    )


class CoupleCreate(CoupleBase):
    pass


class CoupleUpdate(CoupleBase):
    # override
    couple_name: Optional[str]


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
