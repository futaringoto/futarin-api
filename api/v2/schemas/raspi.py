from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

def generate_default_raspiname() -> str:
    return f"raspi_{datetime.now().strftime('%Y%m%d%H%M%S')}"


class RaspiMessageResponse(BaseModel):
    message: str = Field(None, json_schema_extra={"example": "successed!"})


class RaspiBase(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., default_factory=generate_default_raspiname)


class RaspiCreate(RaspiBase):
    id: int


class RaspiUpdate(RaspiBase):
    pass


class RaspiResponse(RaspiBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
    )

