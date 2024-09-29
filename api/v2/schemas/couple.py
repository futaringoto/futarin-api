from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


def generate_default_couplename() -> str:
    return f"couple_{datetime.now().strftime('%Y%m%d%H%M%S')}"


class CoupleBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(default_factory=generate_default_couplename)


class CoupleCreate(CoupleBase):
    pass


class CoupleUpdate(CoupleBase):
    # override
    name: Optional[str]


class CoupleResponse(CoupleBase):
    model_config = ConfigDict(from_attributes=True)
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
